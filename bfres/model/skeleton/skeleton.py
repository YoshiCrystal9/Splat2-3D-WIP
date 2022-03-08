import enum
import io
from typing import List, Tuple

import bfres.core

Matrix3x4 = Tuple[Tuple[float, float, float, float], Tuple[float, float, float, float], Tuple[float, float, float, float]]


class SkeletonFlagsScaling(enum.IntFlag):
    NONE = 0
    STANDARD = 1 << 8
    MAYA = 2 << 8
    SOFTIMAGE = 3 << 8


class SkeletonFlagsRotation(enum.IntFlag):
    QUATERNION = 0
    EULER_XYZ = 1 << 12


class Skeleton(bfres.ResData):
    _SIGNATURE = "FSKL"
    _FLAGS_SCALING_MASK = 0b00000000_00000000_00000011_00000000
    _FLAGS_ROTATION_MASK = 0b00000000_00000000_01110000_00000000

    def __init__(self):
        self._flags: int = 0
        self.bones: List[bfres.Bone] = []
        self.matrix_to_bone_list: List[int] = []
        self.inverse_model_matrices: List[Matrix3x4] = []

    @property
    def flags_scaling(self) -> SkeletonFlagsScaling:
        return SkeletonFlagsScaling(self._flags & self._FLAGS_SCALING_MASK)

    @flags_scaling.setter
    def flags_scaling(self, value: SkeletonFlagsScaling):
        self._flags &= ~self._FLAGS_SCALING_MASK | value

    @property
    def flags_rotation(self) -> SkeletonFlagsRotation:
        return SkeletonFlagsRotation(self._flags & self._FLAGS_ROTATION_MASK)

    @flags_rotation.setter
    def flags_rotation(self, value: SkeletonFlagsRotation):
        self._flags &= ~self._FLAGS_ROTATION_MASK | value

    def load(self, loader: bfres.core.ResFileLoader):
        loader.check_signature(self._SIGNATURE)
        self._flags = loader.read_uint32()
        num_bone = loader.read_uint16()
        num_smooth_matrix = loader.read_uint16()
        num_rigid_matrix = loader.read_uint16()
        loader.seek(2, io.SEEK_CUR)
        self.bones = loader.load_dict(bfres.Bone)
        ofs_bone_list = loader.read_offset()  # Only load dict
        self.matrix_to_bone_list = loader.load_custom(lambda l: l.read_uint16s(num_smooth_matrix + num_rigid_matrix))
        self.inverse_model_matrices = loader.load_custom(lambda l: l.read_matrix3x4s(num_smooth_matrix))
        user_pointer = loader.read_uint32()
