import enum
import io

import bfres.core


class UserData(bfres.ResData):
    def __init__(self):
        self.name = None
        self.value = None
        self.value_type = 0

    def load(self, loader: bfres.core.ResFileLoader):
        self.name = loader.load_string()
        count = loader.read_uint16()
        self.value_type = UserDataType(loader.read_byte())
        loader.seek(1, io.SEEK_CUR)
        if self.value_type == UserDataType.INT32:
            self.value = loader.read_int32s(count)
        elif self.value_type == UserDataType.SINGLE:
            self.value = loader.read_singles(count)
        elif self.value_type == UserDataType.STRING:
            self.value = loader.load_strings(count, "ascii")
        elif self.value_type == UserDataType.WSTRING:
            self.value = loader.load_strings(count, "utf-8")
        elif self.value_type == UserDataType.BYTE:
            self.value = loader.read_bytes(count)


class UserDataType(enum.Enum):
    INT32 = 0
    SINGLE = 1
    STRING = 2
    WSTRING = 3
    BYTE = 4
