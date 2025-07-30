# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import pytest

from qai_hub_models.models.llama_v3_8b_instruct.demo import llama_3_chat_demo


@pytest.mark.skip("#105 move slow_cloud and slow tests to nightly.")
@pytest.mark.slow_cloud
def test_demo() -> None:
    # Run demo and verify it does not crash
    llama_3_chat_demo(is_test=True)
