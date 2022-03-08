from typing import List

import bfres
import bfres.core


class SkeletalAnim(bfres.ResData):
    _SIGNATURE = "FSKA"

    def __init__(self):
        self.name: str = ""
        self.path: str = ""
        self._flags: int = 0
        self.frame_count: int = 0
        self.baked_size: int = 0
        self.bone_anims: List[bfres.BoneAnim] = []
        self.bind_skeleton: bfres.Skeleton = None
        self.bind_indices: List[int] = []
        self.user_data: bfres.ResDict[bfres.UserData] = bfres.ResDict(bfres.UserData)

    def load(self, loader: bfres.core.ResFileLoader):
        loader.check_signature(self._SIGNATURE)
        self.name = loader.load_string()
        self.path = loader.load_string()
        self._flags = loader.read_uint32()
        self.frame_count = loader.read_int32()
        num_bone_anim = loader.read_uint16()
        num_user_data = loader.read_uint16()
        num_curve = loader.read_int32()
        self.baked_size = loader.read_uint32()
        self.bone_anims = loader.load_list(bfres.BoneAnim, num_bone_anim)
        self.bind_skeleton = loader.load(bfres.Skeleton)
        self.bind_indices = loader.load_custom(lambda l: l.read_uint16s(num_bone_anim))
        self.user_data = loader.load_dict(bfres.UserData)
