# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from __future__ import annotations

import gc
import math
from collections.abc import Callable
from typing import Any

import torch

from qai_hub_models.models._shared.llama3.model import (
    Llama3Base,
    RopeEmbedding,
    get_past_keyval_with_shift,
)


def _sample_tokens_from_logits(
    logits: torch.Tensor, top_k: int = 40, top_p: float = 0.95, temp: float = 0.8
) -> torch.Tensor:
    assert logits.ndim == 2

    values, indices = torch.topk(logits, top_k, sorted=True)

    probs = torch.nn.functional.softmax(values, dim=-1)

    is_cut_off = torch.cumsum(probs, dim=-1) > top_p
    if is_cut_off.any():
        cut_off_index = torch.nonzero(is_cut_off)[0, 1].item()
        values = values[:, : cut_off_index + 1]
        indices = indices[:, : cut_off_index + 1]

    probs = torch.nn.functional.softmax(values / temp, dim=-1)

    inner_index = torch.multinomial(probs, num_samples=1).squeeze(1)
    return indices[0][inner_index[0].item()].unsqueeze(0)


class ChatApp:
    """
    This class is a demonstration of how to use Llama model to build a basic ChatApp.
    This App uses two models:
        * Prompt Processor
            - Instantiation with sequence length 128. Used to process user
              prompt.
        * Token Generator
            - Instantiation with sequence length 1. Used to predict
              auto-regressive response.
    """

    def __init__(
        self,
        model_cls: type[Llama3Base],
        get_input_prompt_with_tags: Callable,
        prepare_combined_attention_mask: Callable,
        tokenizer: Any,
        end_tokens: set[str],
        seed: int = 42,
    ):
        """
        Base ChatApp that generates one response for given input token.

            model_cls: Llama Model class that will be used to instantiate model
            get_input_prompt_with_tags: Function to wrap input prompt with appropriate tags
            prepare_combined_attention_mask: Function to combine and build attention mask,
            tokenizer: Tokenizer to use,
            end_tokens: Set of end tokens to convey end of token generation,
        """
        self.model_cls = model_cls
        self.get_input_prompt_with_tags = get_input_prompt_with_tags
        self.prepare_combined_attention_mask = prepare_combined_attention_mask
        self.tokenizer = tokenizer
        self.end_tokens = end_tokens
        self.seed = seed

    def generate_output_prompt(
        self,
        input_prompt: str,
        prompt_sequence_length: int,
        context_length: int,
        max_output_tokens: int,
        bundled_kvcache: bool = True,
    ):
        torch.manual_seed(self.seed)
        input_prompt_processed = self.get_input_prompt_with_tags(
            user_input_prompt=input_prompt
        )

        input_tokens = self.tokenizer(
            input_prompt_processed,
            return_tensors="pt",
            padding="max_length",
            max_length=context_length,
        )
        if context_length % prompt_sequence_length != 0:
            raise ValueError(
                "This script requires the prompt sequence lengths to evenly divide the context length."
            )

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        orig_input_ids = input_tokens["input_ids"].type(torch.long).to(device)

        num_tokens = int(torch.sum(input_tokens["attention_mask"]).item())
        num_prompt_iterations = math.ceil(num_tokens / prompt_sequence_length)

        print(
            f"Will run prompt processor {num_prompt_iterations} time(s) and then token generator."
        )

        # Collect output prompt to summarize later
        output_token = None
        hub_tokens: torch.Tensor | None = None

        model = self.model_cls.from_pretrained(
            sequence_length=prompt_sequence_length,
            context_length=context_length,
        ).to(device)
        rope_embedding = RopeEmbedding(
            max_length=context_length, config=model.llm_config
        )
        is_prompt = True

        # Process input prompt
        input_specs = self.model_cls.get_input_spec(
            sequence_length=prompt_sequence_length,
            context_length=context_length,
        )

        # Initialization of KV cache
        past_key_values = [
            torch.zeros(shape, device=device)
            for k, (shape, _) in input_specs.items()
            if k.startswith("past_")
        ]

        position_ids: torch.Tensor | None = None
        attention_mask: torch.Tensor | None = None
        for i in range(num_prompt_iterations + max_output_tokens - 1):
            if i < num_prompt_iterations:
                seq_len = prompt_sequence_length
                next_seq_len = seq_len if i + 1 < num_prompt_iterations else 1
            else:
                if is_prompt:
                    # switch to token processor
                    model = self.model_cls.from_pretrained(sequence_length=1).to(device)
                    is_prompt = False

                seq_len = 1
                next_seq_len = 1

            if is_prompt:
                input_ids = orig_input_ids[
                    :,
                    max(
                        0, context_length - (num_prompt_iterations - i) * seq_len
                    ) : max(
                        0, context_length - (num_prompt_iterations - i - 1) * seq_len
                    ),
                ]

                # non-padded tokens in first prompt
                first_prompt = (num_tokens - 1) % seq_len + 1
                padding_size0 = seq_len - first_prompt
                padding_size = padding_size0 if i == 0 else 0
                offset = 0 if i == 0 else first_prompt + (i - 1) * seq_len
                position_ids_lst = [0] * (padding_size) + list(
                    range(offset, offset + seq_len - padding_size)
                )
                position_ids = (
                    torch.Tensor(position_ids_lst)
                    .type(torch.long)
                    .reshape(1, seq_len)
                    .to(device)
                )
                position_ids_cos, position_ids_sin = rope_embedding.get_embedding(
                    position_ids,
                )
                attention_mask = torch.zeros((1, context_length), device=device)
                attention_mask[:, context_length - (first_prompt + i * seq_len) :] = 1.0
            else:
                assert output_token is not None
                input_ids = output_token.reshape(-1, 1).type(torch.int32)

                # Shift attention_mask and position_ids
                assert attention_mask is not None
                attention_mask = torch.cat(
                    (
                        attention_mask[:, seq_len:],
                        torch.ones((1, seq_len), device=device),
                    ),
                    dim=-1,
                )
                assert position_ids is not None
                position_ids = (position_ids[:, -1] + 1).reshape(-1, 1)

                position_ids = (
                    torch.Tensor(position_ids).type(torch.long).reshape(1, 1).to(device)
                )
                position_ids_cos, position_ids_sin = rope_embedding.get_embedding(
                    position_ids,
                )

            cm_attention_masks = self.prepare_combined_attention_mask(
                attention_mask=attention_mask,
                input_shape=(1, seq_len),
                past_key_values_length=context_length - seq_len,
            ).to(device)

            # Generate output token
            output = model(
                input_ids,
                cm_attention_masks,
                position_ids_cos,
                position_ids_sin,
                *past_key_values,
            )

            del cm_attention_masks
            del input_ids
            past_key_values = get_past_keyval_with_shift(
                past_key_values,
                output[1:],
                length=context_length - next_seq_len,
            )
            is_prediction = next_seq_len == 1

            if is_prediction:
                # Sample output
                output_token = _sample_tokens_from_logits(output[0][0][[-1]])

                # Assistant generating end of token
                if self.tokenizer.decode(output_token) in self.end_tokens:
                    break

                if is_prompt:
                    hub_tokens = output_token
                else:
                    assert hub_tokens is not None
                    hub_tokens = torch.cat((hub_tokens, output_token), dim=-1)

                print()
                print(f"Text generated so far: {self.tokenizer.decode(hub_tokens)}")
                print()
            gc.collect()

        print("-------- Response Summary --------")
        print(f"Prompt: {input_prompt}")
        print(f"Response: {self.tokenizer.decode(hub_tokens)}")
