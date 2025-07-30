# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from __future__ import annotations

import math
from collections.abc import Callable

import qai_hub as hub
import torch
from torch.nn import CrossEntropyLoss
from tqdm import tqdm

from qai_hub_models.evaluators.base_evaluators import BaseEvaluator, _DataLoader
from qai_hub_models.models._shared.llama3_ao.app import get_past_keyval_with_shift


class PerplexityEvaluator(BaseEvaluator):
    """Evaluator for computing PPL of a Large Language Model.
    This may not be as generic as hoped and may need work. Works with Llama 3.2 3B.

    """

    def __init__(
        self,
        input_specs: hub.InputSpecs,
        context_length: int,
        block_size: int,
        device: torch.device,
    ):
        self.context_length = context_length
        self.block_size = block_size
        self.device = device
        self.past_key_values = []

        # Store KV cache shape
        for k, (shape, _) in input_specs.items():
            if k.startswith("past_"):
                self.past_key_values.append(shape)

        self.reset()

    def add_batch(self, output: list[torch.tensor], gt: torch.tensor):
        self.batch_index += 1
        logits = output[0]
        # This kv cache is needed to maintain the context between multiple blocks.
        num_blocks = self.context_length // self.block_size
        self.kv_cache: list[torch.tensor] = (
            [torch.zeros(shape) for shape in self.past_key_values]
            if self.batch_index % num_blocks == 0
            else get_past_keyval_with_shift(
                self.kv_cache, output[1:], length=self.context_length - self.block_size
            )
        )
        lm_logits = logits.reshape(1, -1, logits.shape[-1])
        shift_logits = lm_logits[..., :-1, :].contiguous().to(dtype=torch.float32)
        shift_labels = gt[..., 1:].contiguous().to(shift_logits.device)
        loss_fct = CrossEntropyLoss()
        loss_value = loss_fct(
            shift_logits.view(-1, shift_logits.size(-1)),
            shift_labels.view(-1),
        ).item()
        self.loss += loss_value

    def reset(self):
        self.loss = 0.0
        self.batch_index = 0
        self.kv_cache = [torch.zeros(shape) for shape in self.past_key_values]

    def get_accuracy_score(self) -> float:
        average_loss = self.loss / self.batch_index
        return math.exp(average_loss)

    def formatted_accuracy(self) -> str:
        return f"PPL (lower is better): {self.get_accuracy_score():.2f}"

    def for_each_batch(
        self,
        model: torch.nn.Module,
        data: _DataLoader,
        num_samples: int | None = None,
        callback: Callable[
            [list[torch.tensor], list[torch.tensor], list[torch.tensor]], None
        ]
        | None = None,
    ) -> None:
        model.to(self.device)
        total_samples = 0
        batch_size = 1
        num_samples = num_samples or len(data)
        with tqdm(
            total=num_samples,
            desc="Number of samples completed",
        ) as pbar:
            for sample in data:
                inputs, ground_truth, *_ = sample
                inputs = list(inputs)
                inputs.extend(self.kv_cache)
                inputs = [input.to(self.device) for input in inputs]
                outputs = model(*inputs)
                assert isinstance(ground_truth, torch.Tensor)
                ground_truth = ground_truth.to(self.device)
                if callback:
                    callback(inputs, outputs, ground_truth)
                total_samples += 1
                pbar.update(batch_size)
                if total_samples >= num_samples:
                    break

    def add_from_dataset(
        self,
        model: torch.nn.Module,
        data: _DataLoader,
        eval_iterations: int | None = None,
    ) -> None:
        def _add_batch(
            _: torch.Tensor, outputs: torch.Tensor, ground_truth: torch.Tensor
        ):
            self.add_batch(outputs, ground_truth)

        self.for_each_batch(model, data, eval_iterations, _add_batch)
