import enum
from typing import Tuple

import bfres.core
from bfres.core.bits import has_flag

Vector3F = Tuple[float, float, float]
Vector4F = Tuple[float, float, float, float]


class BoneAnimDataOffset(enum.IntEnum):
    FLAGS = 0x00
    SCALE_X = 0x04
    SCALE_Y = 0x08
    SCALE_Z = 0x0C
    TRANSLATE_X = 0x10
    TRANSLATE_Y = 0x14
    TRANSLATE_Z = 0x18
    # PADDING = 0x1C
    ROTATE_X = 0x20
    ROTATE_Y = 0x24
    ROTATE_Z = 0x28
    ROTATE_W = 0x2C


class BoneAnimData:
    def __init__(self, loader: bfres.core.ResFileLoader, flags_base: bfres.BoneAnimFlagsBase):
        self.flags: int = 0  # Never in files
        self.scale: Vector3F = loader.read_vector3f() if has_flag(flags_base, bfres.BoneAnimFlagsBase.SCALE) \
            else (0, 0, 0)
        self.translate: Vector3F = loader.read_vector3f() if has_flag(flags_base, bfres.BoneAnimFlagsBase.TRANSLATE) \
            else (0, 0, 0)
        self.padding: int = 0  # Never in files
        self.rotate: Vector4F = loader.read_vector4f() if has_flag(flags_base, bfres.BoneAnimFlagsBase.ROTATE) \
            else (0, 0, 0, 0)
