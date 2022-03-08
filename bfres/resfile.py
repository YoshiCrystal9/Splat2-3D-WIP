from enum import Enum

import bfres.core


class ByteOrder(Enum):
    BIG_ENDIAN = 0xFEFF
    LITTLE_ENDIAN = 0xFFFE


class ResFile(bfres.ResData):
    """Represents a NintendoWare for Cafe (NW4F) graphics data archive file."""

    _SIGNATURE = "FRES"

    def __init__(self, raw):
        self.version: int = 0
        self.byte_order: ByteOrder = ByteOrder.LITTLE_ENDIAN
        self.alignment: int = 0
        self.name: str = ""
        self.models: bfres.ResDict[bfres.Model] = None
        self.textures: bfres.ResDict[bfres.Texture] = None
        # self.skeletal_anims: bfres.ResDict = None
        # self.shader_param_anims: bfres.ResDict = None
        # self.color_anims: bfres.ResDict = None
        # self.tex_srt_anims: bfres.ResDict = None
        # self.tex_pattern_anims: bfres.ResDict = None
        # self.bone_visibility_anims: bfres.ResDict = None
        # self.mat_visibility_anims: bfres.ResDict = None
        # self.shape_anims: bfres.ResDict = None
        # self.scene_anims: bfres.ResDict = None
        # self.external_files: bfres.ResDict = None
        loader = bfres.core.ResFileLoader(self, raw)
        loader.execute()

    def load(self, loader: bfres.core.ResFileLoader):
        loader.check_signature(self._SIGNATURE)
        self.version = loader.read_uint32()
        self.byte_order = ByteOrder(loader.read_uint16())
        siz_header = loader.read_uint16()
        siz_file = loader.read_uint32()
        self.alignment = loader.read_uint32()
        self.name = loader.load_string()
        siz_string_pool = loader.read_uint32()
        ofs_string_pool = loader.read_offset()
        self.models = loader.load_dict(bfres.Model)
        self.textures = loader.load_dict(bfres.Texture)
        # self.skeletal_anims = loader.load_dict()
        # self.shader_param_anims = loader.load_dict()
        # self.color_anims = loader.load_dict()
        # self.tex_srt_anims = loader.load_dict()
        # self.tex_pattern_anims = loader.load_dict()
        # self.bone_visibility_anims = loader.load_dict()
        # self.mat_visibility_anims = loader.load_dict()
        # self.shape_anims = loader.load_dict()
        # self.scene_anims = loader.load_dict()
        # self.external_files = loader.load_dict()
        # num_model = loader.read_uint16()
        # num_texture = loader.read_uint16()
        # num_skeletal_anim = loader.read_uint16()
        # num_shader_param_anim = loader.read_uint16()
        # num_color_anim = loader.read_uint16()
        # num_tex_srt_anim = loader.read_uint16()
        # num_tex_pattern_anim = loader.read_uint16()
        # num_bone_visibility_anim = loader.read_uint16()
        # num_mat_visibility_anim = loader.read_uint16()
        # num_shape_anim = loader.read_uint16()
        # num_scene_anim = loader.read_uint16()
        # num_external_file = loader.read_uint16()
        # user_pointer = loader.read_uint32()
