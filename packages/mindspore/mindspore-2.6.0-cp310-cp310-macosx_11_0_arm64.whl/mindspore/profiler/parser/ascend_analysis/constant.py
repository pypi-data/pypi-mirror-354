# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Constant value for ascend profiling parser."""
import os


class Constant:
    """Constant values"""

    HOST_TO_DEVICE = "HostToDevice"
    START_FLOW = "s"
    END_FLOW = "f"
    META_EVENT = 'M'
    COMPLETE_EVENT = 'X'
    FLOW_OP = "flow"
    INVALID_FLOW_ID = 18446744073709551615
    DEFAULT_PROCESS_NUMBER = os.cpu_count() // 2

    # file authority
    MAX_FILE_SIZE = 1024 * 1024 * 1024 * 10
    MAX_CSV_SIZE = 1024 * 1024 * 1024 * 5

    # tlv constant struct
    FIX_SIZE_BYTES = "fix_size_bytes"
    NS_TO_US = 1e-3

    # field name
    SEQUENCE_UNMBER = "Sequence number"
    FORWORD_THREAD_ID = "Fwd thread id"
    OP_NAME = "op_name"
    INPUT_SHAPES = "Input Dims"
    INPUT_DTYPES = "Input type"
    CALL_STACK = "Call stack"
    MODULE_HIERARCHY = "Module Hierarchy"
    FLOPS = "flops"
    NAME = "name"
    CUSTOM_INFO = "custom_info"

    # trace constant
    PROCESS_NAME = "process_name"
    PROCESS_LABEL = "process_labels"
    PROCESS_SORT = "process_sort_index"
    THREAD_NAME = "thread_name"
    THREAD_SORT = "thread_sort_index"

    # dir name
    FRAMEWORK_DIR = "FRAMEWORK"
    PROFILER_DIR = "profiler"
    TOP_SCOPE_NAMES = ('Default', 'Gradients', 'recompute_Default')

    # the index of modules of timeline
    MINDSPORE = 1
    CPU_OP = 2
    CANN = 3
    SCOPE_LAYLER = 4
    ASCEND_HARDWARE = 5
    HCCL = 6
    OVERLAP = 7
    OTHERWISE = 8
