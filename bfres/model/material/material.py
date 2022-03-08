from typing import List

import enum
import math

import bfres
import bfres.core


class Material(bfres.ResData):
    def __init__(self):
        self.name: str = ""
        self.flags: MaterialFlags = MaterialFlags.NONE
        self.render_infos: bfres.ResDict[bfres.RenderInfo] = bfres.ResDict(bfres.RenderInfo)
        self.render_state: bfres.RenderState = None
        self.shader_assign: bfres.ShaderAssign = None
        self.texture_refs: List[bfres.TextureRef] = []
        self.samplers: bfres.ResDict[bfres.Sampler] = bfres.ResDict(bfres.Sampler)
        self.shader_params: bfres.ResDict[bfres.ShaderParam] = bfres.ResDict(bfres.ShaderParam)
        self.shader_param_data: bytes = None
        self.user_data: bfres.ResDict[bfres.UserData] = bfres.ResDict(bfres.UserData)
        self.volatile_flags: bytes = None

    def load(self, loader: bfres.core.ResFileLoader):
        loader.check_signature("FMAT")
        self.name = loader.load_string()
        self.flags = MaterialFlags(loader.read_uint32())
        idx = loader.read_uint16()
        num_render_info = loader.read_uint16()
        num_sampler = loader.read_byte()
        num_texture_ref = loader.read_byte()
        num_shader_param = loader.read_uint16()
        num_shader_param_volatile = loader.read_uint16()
        siz_param_source = loader.read_uint16()
        siz_param_raw = loader.read_uint16()
        num_user_data = loader.read_uint16()
        self.render_infos = loader.load_dict(bfres.RenderInfo)
        self.render_state = loader.load(bfres.RenderState)
        self.shader_assign = loader.load(bfres.ShaderAssign)
        self.texture_refs = loader.load_list(bfres.TextureRef, num_texture_ref)
        ofs_sampler_list = loader.read_offset()  # Only use dict.
        self.samplers = loader.load_dict(bfres.Sampler)
        ofs_shader_param_list = loader.read_offset()
        self.shader_params = loader.load_dict(bfres.ShaderParam)
        self.shader_param_data = loader.load_custom(lambda l: l.read_bytes(siz_param_source))
        self.user_data = loader.load_dict(bfres.UserData)
        self.volatile_flags = loader.load_custom(lambda l: l.read_bytes(math.ceil(num_shader_param / 8)))
        user_pointer = loader.read_uint32()


class MaterialFlags(enum.IntEnum):
    NONE = 0
    VISIBLE = 1
