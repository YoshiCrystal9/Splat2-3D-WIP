import enum
from typing import Tuple

import bfres
import bfres.core


class BoneFlags(enum.IntFlag):
    NONE = 0
    VISIBLE = 1 << 0


class BoneFlagsRotation(enum.IntFlag):
    QUATERNION = 0
    EULER_XYZ = 1 << 12


class BoneFlagsBillboard(enum.IntFlag):
    NONE = 0
    CHILD = 1 << 16
    WORLD_VIEW_VECTOR = 2 << 16
    WORLD_VIEW_POINT = 3 << 16
    SCREEN_VIEW_VECTOR = 4 << 16
    SCREEN_VIEW_POINT = 5 << 16
    YAXIS_VIEW_VECTOR = 6 << 16
    YAXIS_VIEW_POINT = 7 << 16


class BoneFlagsTransform(enum.IntFlag):
    NONE = 0
    SCALE_UNIFORM = 1 << 24
    SCALE_VOLUME_ONE = 1 << 25
    ROTATE_ZERO = 1 << 26
    TRANSLATE_ZERO = 1 << 27
    SCALE_ONE = SCALE_UNIFORM | SCALE_VOLUME_ONE
    ROTATE_TRANSLATE_ZERO = ROTATE_ZERO | TRANSLATE_ZERO
    IDENTITY = SCALE_ONE | ROTATE_ZERO | TRANSLATE_ZERO


class BoneFlagsTransformCumulative(enum.IntFlag):
    NONE = 0
    SCALE_UNIFORM = 1 << 28
    SCALE_VOLUME_ONE = 1 << 29
    ROTATE_ZERO = 1 << 30
    TRANSLATE_ZERO = 1 << 31
    SCALE_ONE = SCALE_UNIFORM | SCALE_VOLUME_ONE
    ROTATE_TRANSLATE_ZERO = ROTATE_ZERO | TRANSLATE_ZERO
    IDENTITY = SCALE_ONE | ROTATE_ZERO | TRANSLATE_ZERO


class Bone(bfres.ResData):
    _FLAGS_MASK = 0b00000000_00000000_00000000_00000001
    _FLAGS_MASK_ROTATE = 0b00000000_00000000_01110000_00000000
    _FLAGS_MASK_BILLBOARD = 0b00000000_00000111_00000000_00000000
    _FLAGS_MASK_TRANSFORM = 0b00001111_00000000_00000000_00000000
    _FLAGS_MASK_TRANSFORM_CUMULATIVE = 0b11110000_00000000_00000000_00000000

    def __init__(self):
        self.name: str = ""
        self.parent_index: int = 0xFFFF
        self.smooth_matrix_index: int = -1
        self.rigid_matrix_index: int = -1
        self.billboard_index: int = 0xFFFF
        self._flags: int = 0
        self.scale: Tuple[float, float, float] = (1, 1, 1)
        self.rotation: Tuple[float, float, float, float] = (0, 0, 0, 0)
        self.position: Tuple[float, float, float] = (0, 0, 0)
        self.user_data: bfres.ResDict[bfres.UserData] = bfres.ResDict(bfres.UserData)

    @property
    def flags(self) -> BoneFlags:
        return BoneFlags(self._flags & self._FLAGS_MASK)

    @flags.setter
    def flags(self, value: BoneFlags):
        self._flags &= ~self._FLAGS_MASK | value

    @property
    def flags_rotate(self) -> BoneFlagsRotation:
        return BoneFlagsRotation(self._flags & self._FLAGS_MASK_ROTATE)

    @flags_rotate.setter
    def flags_rotate(self, value: BoneFlagsRotation):
        self._flags &= ~self._FLAGS_MASK_ROTATE | value

    @property
    def flags_billboard(self) -> BoneFlagsBillboard:
        return BoneFlagsBillboard(self._flags & self._FLAGS_MASK_BILLBOARD)

    @flags_billboard.setter
    def flags_billboard(self, value: BoneFlagsBillboard):
        self._flags &= ~self._FLAGS_MASK_BILLBOARD | value

    @property
    def flags_transform(self) -> BoneFlagsTransform:
        return BoneFlagsTransform(self._flags & self._FLAGS_MASK_TRANSFORM)

    @flags_transform.setter
    def flags_transform(self, value: BoneFlagsTransform):
        self._flags &= ~self._FLAGS_MASK_TRANSFORM | value

    @property
    def flags_transform_cumulative(self) -> BoneFlagsTransformCumulative:
        return BoneFlagsTransformCumulative(self._flags & self._FLAGS_MASK_TRANSFORM_CUMULATIVE)

    @flags_transform_cumulative.setter
    def flags_transform_cumulative(self, value: BoneFlagsTransformCumulative):
        self._flags &= ~self._FLAGS_MASK_TRANSFORM_CUMULATIVE | value

    def load(self, loader: bfres.core.ResFileLoader):
        self.name = loader.load_string()
        idx = loader.read_uint16()
        self.parent_index = loader.read_uint16()
        self.smooth_matrix_index = loader.read_int16()
        self.rigid_matrix_index = loader.read_int16()
        self.billboard_index = loader.read_uint16()
        num_user_data = loader.read_uint16()
        self._flags = loader.read_uint32()
        self.scale = loader.read_vector3f()
        self.rotation = loader.read_vector4f()
        self.position = loader.read_vector3f()
        self.user_data = loader.load_dict(bfres.UserData)
