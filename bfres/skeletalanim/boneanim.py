import enum
from typing import List

import bfres.core


class BoneAnimFlagsBase(enum.IntFlag):
    SCALE = 1 << 3
    ROTATE = 1 << 4
    TRANSLATE = 1 << 5


class BoneAnimFlagsCurve(enum.IntFlag):
    SCALE_X = 1 << 6
    SCALE_Y = 1 << 7
    SCALE_Z = 1 << 8
    ROTATE_X = 1 << 9
    ROTATE_Y = 1 << 10
    ROTATE_Z = 1 << 11
    ROTATE_W = 1 << 12
    TRANSLATE_X = 1 << 13
    TRANSLATE_Y = 1 << 14
    TRANSLATE_Z = 1 << 15


class BoneAnimFlagsTransform(enum.IntFlag):  # Same as BoneFlagsTransform
    SEGMENT_SCALE_COMPENSATE = 1 << 23
    SCALE_UNIFORM = 1 << 24
    SCALE_VOLUME_ONE = 1 << 25
    ROTATE_ZERO = 1 << 26
    TRANSLATE_ZERO = 1 << 27
    SCALE_ONE = SCALE_VOLUME_ONE | SCALE_UNIFORM
    ROTATE_TRANSLATE_ZERO = ROTATE_ZERO | TRANSLATE_ZERO
    IDENTITY = SCALE_ONE | ROTATE_ZERO | TRANSLATE_ZERO


class BoneAnim(bfres.ResData):
    _FLAGS_MASK_BASE = 0b00000000_00000000_00000000_00111000
    _FLAGS_MASK_CURVE = 0b00000000_00000000_11111111_11000000
    _FLAGS_MASK_TRANSFORM = 0b00001111_10000000_00000000_00000000

    def __init__(self):
        self._flags: int = 0
        self.name: str = ""
        self.begin_rotate: int = 0
        self.begin_translate: int = 0
        self.begin_base_translate: int = 0
        self.begin_curve: int = 0
        self.curves: List[bfres.AnimCurve] = []
        self.base_data: bfres.BoneAnimData = []

    @property
    def flags_base(self) -> BoneAnimFlagsBase:
        return BoneAnimFlagsBase(self._flags & self._FLAGS_MASK_BASE)

    @flags_base.setter
    def flags_base(self, value: BoneAnimFlagsBase):
        self._flags &= ~self._FLAGS_MASK_BASE | value

    @property
    def flags_curve(self) -> BoneAnimFlagsCurve:
        return BoneAnimFlagsCurve(self._flags & self._FLAGS_MASK_CURVE)

    @flags_curve.setter
    def flags_curve(self, value: BoneAnimFlagsCurve):
        self._flags &= ~self._FLAGS_MASK_CURVE | value

    @property
    def flags_transform(self) -> BoneAnimFlagsTransform:
        return BoneAnimFlagsTransform(self._flags & self._FLAGS_MASK_TRANSFORM)

    @flags_transform.setter
    def flags_transform(self, value: BoneAnimFlagsTransform):
        self._flags &= ~self._FLAGS_MASK_TRANSFORM | value

    def load(self, loader: bfres.core.ResFileLoader):
        self._flags = loader.read_uint32()
        self.name = loader.load_string()
        self.begin_rotate = loader.read_byte()
        self.begin_translate = loader.read_byte()
        num_curve = loader.read_byte()
        self.begin_base_translate = loader.read_byte()
        self.begin_curve = loader.read_byte()
        self.curves = loader.load_list(bfres.AnimCurve, num_curve)
        self.base_data = loader.load_custom(lambda l: bfres.BoneAnimData(loader, self.flags_base))
