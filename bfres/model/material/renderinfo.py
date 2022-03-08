from typing import List, Union

import enum
import io

import bfres.core


class RenderInfoType(enum.IntEnum):
    INT32 = 0
    SINGLE = 1
    STRING = 2


class RenderInfo(bfres.ResData):
    def __init__(self):
        self.value_type: RenderInfoType = RenderInfoType.INT32
        self.name: str = ""
        self.value: Union[List[int], List[float], List[str]] = None

    def load(self, loader: bfres.core.ResFileLoader):
        count = loader.read_uint16()
        self.value_type = RenderInfoType(loader.read_byte())
        loader.seek(1, io.SEEK_CUR)
        self.name = loader.load_string()
        if self.value_type == RenderInfoType.INT32:
            self.value = loader.read_int32s(count)
        elif self.value_type == RenderInfoType.SINGLE:
            self.value = loader.read_singles(count)
        elif self.value_type == RenderInfoType.STRING:
            self.value = loader.load_strings(count)
