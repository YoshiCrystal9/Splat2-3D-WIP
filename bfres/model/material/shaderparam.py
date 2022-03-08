import enum
import io

import bfres.core


class ShaderParamType(enum.IntEnum):
    BOOL = 0
    BOOL_2 = 1
    BOOL_3 = 2
    BOOL_4 = 3
    INT = 4
    INT_2 = 5
    INT_3 = 6
    INT_4 = 7
    UINT = 8
    UINT_2 = 9
    UINT_3 = 10
    UINT_4 = 11
    FLOAT = 12
    FLOAT_2 = 13
    FLOAT_3 = 14
    FLOAT_4 = 15
    RESERVED_2 = 16
    FLOAT_2X2 = 17
    FLOAT_2X3 = 18
    FLOAT_2X4 = 19
    RESERVED_3 = 20
    FLOAT_3X2 = 21
    FLOAT_3X3 = 22
    FLOAT_3X4 = 23
    RESERVED_4 = 24
    FLOAT_4X2 = 25
    FLOAT_4X3 = 26
    FLOAT_4X4 = 27
    SRT_2D = 28
    SRT_3D = 29
    TEX_SRT = 30
    TEX_SRT_EX = 31


class ShaderParam(bfres.ResData):
    def __init__(self):
        self.value_type: ShaderParamType = ShaderParamType.BOOL
        self.data_offset: int = 0
        self.depended_index: int = 0
        self.depend_index: int = 0
        self.name: str = ""

    def load(self, loader: bfres.core.ResFileLoader):
        self.value_type = ShaderParamType(loader.read_byte())
        if loader.res_file.version >= 0x03030000:
            siz_data = loader.read_byte()
            self.data_offset = loader.read_uint16()
            offset = loader.read_int32()  # Uniform variable offset.
            callback_pointer = loader.read_uint32()
            self.depended_index = loader.read_uint16()
            self.depend_index = loader.read_uint16()
            self.name = loader.load_string()
        else:
            # GUESS
            loader.seek(1, io.SEEK_CUR)
            self.data_offset = loader.read_uint16()
            offset = loader.read_int32()  # Uniform variable offset.
            self.name = loader.load_string()
