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
"""Function event data struct."""
from typing import Dict, Optional
from enum import Enum
from decimal import Decimal
import struct
from abc import ABC, abstractmethod

from mindspore.profiler.parser.ascend_analysis.constant import Constant
from mindspore.profiler.parser.ascend_analysis.profiler_info_parser import ProfilerInfoParser


class BaseEvent(ABC):
    """Base class of CANNEvent and MindSporeOpEvent"""

    def __init__(self, data: Dict):
        if not isinstance(data, dict):
            raise TypeError("Input data must be dict.")
        # common attributes
        self._orig_data = data
        self.name: str = ""
        self.pid: int = 0
        self.tid: int = 0
        self.ts: Decimal = Decimal(0)
        self.te: Decimal = Decimal(0)
        self.dur: float = 0.0
        self.args: Dict = {}
        self.parent: Optional[BaseEvent] = None
        self._init_params()

    @abstractmethod
    def _init_params(self):
        err_msg = "Protected function _init_params need to be implemented."
        raise NotImplementedError(err_msg)


class CANNEvent(BaseEvent):
    """Function event collected on the CANN side"""

    def _init_params(self):
        """Initialize the attribute value of CANNEvent."""
        self.ts = Decimal(str(self._orig_data.get("ts", 0)))
        self.pid = self._orig_data.get("pid", 0)
        self.tid = self._orig_data.get("tid", 0)
        self.dur = self._orig_data.get("dur", 0.0)
        self.te = self.ts + Decimal(str(self.dur))
        self.name = self._orig_data.get("name", "")
        self.id = self._orig_data.get("id", 0)
        self.args = self._orig_data.get("args", {})
        self.ph = self._orig_data.get("ph")
        self.cat = self._orig_data.get("cat")

    def is_flow_start_event(self) -> bool:
        """Determine whether the event is flow start event or not."""
        return self._orig_data.get("cat") == Constant.HOST_TO_DEVICE and \
               self._orig_data.get("ph") == Constant.START_FLOW

    def is_flow_end_event(self) -> bool:
        """Determine whether the event is flow end event or not."""
        return self._orig_data.get("cat") == Constant.HOST_TO_DEVICE and \
               self._orig_data.get("ph") == Constant.END_FLOW

    def is_x_event(self) -> bool:
        """Determine whether the event x event or not."""
        return self._orig_data.get("ph") == Constant.COMPLETE_EVENT

    def get_sort_index(self):
        """get the process sort index"""
        if self.args.get('name', '') == 'Ascend Hardware':
            return Constant.ASCEND_HARDWARE
        if self.args.get('name', '') == 'CANN':
            return Constant.CANN
        if self.args.get('name', '') == 'HCCL':
            return Constant.HCCL
        if self.args.get('name', '') == 'Overlap Analysis':
            return Constant.OVERLAP
        return Constant.OTHERWISE

    def to_json(self):
        """Cast to trace event."""
        if self.ph == Constant.META_EVENT:
            if self.name == Constant.PROCESS_NAME:
                return [{'name': self.name, 'pid': self.pid, 'tid': self.tid,
                         'args': self.args, 'ph': self.ph},
                        {'name': Constant.PROCESS_SORT, 'pid': self.pid, 'tid': self.tid,
                         'args': {'sort_index': self.get_sort_index()}, 'ph': self.ph}]
            if self.name == Constant.PROCESS_SORT:
                return None
            return {'name': self.name, 'pid': self.pid, 'tid': self.tid,
                    'args': self.args, 'ph': self.ph}

        if self.ph == Constant.COMPLETE_EVENT:
            if self.parent is not None:
                self.args.update({'mindspore_op': self.parent.name})
            res = {'name': self.name, 'pid': self.pid, 'tid': self.tid,
                   'ts': str(self.ts), 'dur': self.dur, 'args': self.args, 'ph': self.ph}
            if self.cat:
                res.update({'cat': self.cat})
            return res

        if self.ph == Constant.START_FLOW:
            return {"ph": self.ph, "name": self.name, "id": self.id, "pid": self.pid,
                    "tid": self.tid, "ts": str(self.ts), "cat": self.cat}

        if self.ph == Constant.END_FLOW:
            return {"ph": self.ph, "name": self.name, "id": self.id, "pid": self.pid,
                    "tid": self.tid, "ts": str(self.ts), "cat": self.cat, 'bp': "e"}
        return None


class MindSporeOpEnum(Enum):
    """MindSporeOp index enum"""
    START_NS = 0
    END_NS = 1
    SEQUENCE_UNMBER = 2
    PROCESS_ID = 3
    START_THREAD_ID = 4
    END_THREAD_ID = 5
    FORWORD_THREAD_ID = 6
    FLOW_ID = 7
    STEP_ID = 8
    LEVEL = 9
    IS_ASYNC = 10


class MindSporeOpEvent(BaseEvent):
    """
    Function event collected on the mindspore frame side.

    Args:
        data(Dict): The mindspore frame side data decoded by TLVDecoder.
    """
    _tlv_type_dict = {
        Constant.OP_NAME: 3, Constant.INPUT_SHAPES: 5, Constant.INPUT_DTYPES: 4,
        Constant.CALL_STACK: 6, Constant.MODULE_HIERARCHY: 7, Constant.FLOPS: 8,
        Constant.CUSTOM_INFO: 9
    }
    _fix_data_format = "<3q6Qb?"

    def _init_params(self):
        """Initialize the attribute value of MindSporeOpEvent."""
        fix_size_data = struct.unpack(self._fix_data_format, self._orig_data.get(Constant.FIX_SIZE_BYTES))
        self.pid = Constant.MINDSPORE
        self.tid = int(fix_size_data[MindSporeOpEnum.START_THREAD_ID.value])
        self.name = str(self._orig_data.get(self._tlv_type_dict.get(Constant.OP_NAME), ""))
        self.ts = ProfilerInfoParser.get_local_time(fix_size_data[MindSporeOpEnum.START_NS.value])  # unit is us
        self.te = ProfilerInfoParser.get_local_time(fix_size_data[MindSporeOpEnum.END_NS.value])  # unit is us
        self.dur = self.te - self.ts
        self.flow_id = int(fix_size_data[MindSporeOpEnum.FLOW_ID.value])
        self.step = int(fix_size_data[MindSporeOpEnum.STEP_ID.value])
        self.level = int(fix_size_data[MindSporeOpEnum.LEVEL.value])
        self.custom_info = ""
        self.args = self._get_args(fix_size_data)

    def _get_args(self, fix_size_data) -> Dict:
        """Get the rest information saved in args"""
        args = {
            Constant.SEQUENCE_UNMBER: int(fix_size_data[MindSporeOpEnum.SEQUENCE_UNMBER.value]),
            Constant.FORWORD_THREAD_ID: int(fix_size_data[MindSporeOpEnum.FORWORD_THREAD_ID.value])}
        for type_name, type_id in self._tlv_type_dict.items():
            if type_name == Constant.OP_NAME or type_id not in self._orig_data.keys():
                continue
            if type_name in set([Constant.INPUT_SHAPES, Constant.INPUT_DTYPES, Constant.CALL_STACK]):
                args[type_name] = self._orig_data.get(type_id).replace("|", "\r\n")
            elif type_name == Constant.CUSTOM_INFO and self._orig_data.get(type_id):
                pairs = self._orig_data.get(type_id).split(';')
                custom_info = {pair.split(':')[0]: pair.split(':')[1] for pair in pairs}
                args[type_name] = custom_info
                self.custom_info = custom_info.__str__()
            else:
                args[type_name] = self._orig_data.get(type_id)
        return args
