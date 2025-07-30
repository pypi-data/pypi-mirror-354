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
"""The parser for integrating data from the framework side and CANN side."""
from collections import defaultdict
from typing import List, Tuple, Optional
from decimal import Decimal

from mindspore import log as logger
from mindspore.profiler.common.validator.validate_path import validate_and_normalize_path
from mindspore.profiler.parser.ascend_analysis.function_event import CANNEvent, MindSporeOpEvent
from mindspore.profiler.parser.ascend_analysis.fwk_file_parser import FwkFileParser
from mindspore.profiler.parser.ascend_analysis.trace_event_manager import TraceEventManager
from mindspore.profiler.parser.ascend_analysis.msprof_timeline_parser import MsprofTimelineParser
from mindspore.profiler.parser.ascend_analysis.profiler_info_parser import ProfilerInfoParser
from mindspore.profiler.parser.profiler_info import ProfilerInfo


class FwkCANNParser:
    """The top-level trace view parser."""

    def __init__(self, source_path: str, msprof_data: List, rank_id: int, step_list=None):
        source_path = validate_and_normalize_path(source_path)
        ProfilerInfoParser.init_source_path(source_path)
        ProfilerInfoParser.init_rank_id(rank_id)

        fwk_parser = FwkFileParser(source_path, rank_id)
        self._fwk_data = fwk_parser.get_op_range_data(step_list)
        self._fwk_json, self._link_event_dict, self._fwk_launch_op = fwk_parser.get_fwk_trace_data(self._fwk_data)

        msprof_timeline_parser = MsprofTimelineParser(msprof_data)
        self._start_flow_to_npu_dict, self._device_mostly_json, self.scope_data_without_flow \
            = msprof_timeline_parser.get_acl_to_npu_data()
        self.scope_data_with_flow = []
        self.rank_id: int = rank_id
        self.kernels: List[CANNEvent] = []

    def generate_trace_data(self):
        """
        Generate trace view json timeline file which contains framework side and
        device side data.
        """
        fwk_flow_json = self.__link_msop_self()
        device_flow_and_x_json = self.__link_msop_kernel()
        return self._fwk_json + fwk_flow_json + self._device_mostly_json + device_flow_and_x_json

    def __link_msop_self(self):
        """Create flow between framework-side multi-level pipeline task."""
        flow_json = []
        for op_data_list in self._link_event_dict.values():
            if len(op_data_list) != 2:
                logger.info('Only alow 2 op_data have the same flow_id. but got %s', len(op_data_list))
                continue
            flow_json.extend(TraceEventManager.create_mindspore_to_self_flow(op_data_list[0],
                                                                             op_data_list[1]))
        return flow_json

    def __link_msop_kernel(self):
        """Associate the frame-side operator with the device-side kernel"""
        trace_data_json = []
        acl_to_npu_by_tid = {}
        for (cann_op_tid, cann_op_ts), event_list in self._start_flow_to_npu_dict.items():
            acl_to_npu_by_tid.setdefault(cann_op_tid, defaultdict(list))[cann_op_ts].extend(event_list)

        if self._fwk_launch_op and acl_to_npu_by_tid and self._fwk_launch_op.keys() != acl_to_npu_by_tid.keys():
            logger.warning("Failed to create link between mindspore operator and kernels.")
        is_not_O2 = bool(ProfilerInfo.get_profiler_info().get(ProfilerInfo.JIT_LEVEL, "") != "O2")
        for device_tid in acl_to_npu_by_tid:
            host_data_sorted = sorted(self._fwk_launch_op.get(device_tid, []), key=lambda x: x.ts)
            op_idx = 0

            for ts, device_data_list in sorted(acl_to_npu_by_tid.get(device_tid).items(), key=lambda x: x[0]):
                op_idx, status = FwkCANNParser.__find_launch_op(ts, host_data_sorted, op_idx)
                if not status and is_not_O2:
                    logger.warning("There are %s device ops have no flows were found. The CANN ts is %s.",
                                   len(device_data_list), ts)

                for device_data in device_data_list:
                    if status:
                        device_data.parent = host_data_sorted[op_idx]
                        trace_data_json.extend(TraceEventManager.create_mindspore_to_npu_flow(device_data.parent,
                                                                                              device_data))
                        self.kernels.append(device_data)

                    scope_layer = MsprofTimelineParser.parse_ascend_hardware_scope(device_data)

                    if scope_layer is not None:
                        self.scope_data_with_flow.append(scope_layer)

                    event_json = device_data.to_json()
                    if event_json and isinstance(event_json, list):
                        trace_data_json.extend(event_json)
                    elif event_json and isinstance(event_json, dict):
                        trace_data_json.append(event_json)

        return trace_data_json

    @staticmethod
    def __find_launch_op(ts: Decimal, op_list: List[MindSporeOpEvent],
                         left: Optional[int] = None, right: Optional[int] = None
                         ) -> Tuple[int, bool]:
        """
        Searching the op_list in [left, right) range and find the operator
        whose start time is larger than ts and end time is less than ts.

        Args:
            ts(Decimal): kernel start time
            op_list(List): MindSporeOpEvent list
            left & right(int): the searching index range is [left, right)

        Return:
            Tuple[int, bool]: the first element is the searched index, the second element
                marks where the operator index is found or not.
        """
        left = 0 if (left is None or left < 0) else left
        right = len(op_list) if (right is None or right < 0) else right
        # The data in range [left, right) is considered.
        while right > left:
            if op_list[left].ts > ts:
                return left, False
            if op_list[left].te < ts:
                left += 1
            else:
                return left, True
        return left, False
