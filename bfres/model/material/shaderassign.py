import bfres
import bfres.core


class ShaderAssign(bfres.ResData):
    def __init__(self):
        self.shader_archive_name: str = ""
        self.shading_model_name: str = ""
        self.revision: int = 0
        self.attrib_assigns: bfres.ResDict[bfres.ResString] = bfres.ResDict(bfres.ResString)
        self.sampler_assigns: bfres.ResDict[bfres.ResString] = bfres.ResDict(bfres.ResString)
        self.shader_options: bfres.ResDict[bfres.ResString] = bfres.ResDict(bfres.ResString)

    def load(self, loader: bfres.core.ResFileLoader):
        self.shader_archive_name = loader.load_string()
        self.shading_model_name = loader.load_string()
        self.revision = loader.read_uint32()
        num_attrib_assign = loader.read_byte()
        num_sampler_assign = loader.read_byte()
        num_shader_option = loader.read_uint16()
        self.attrib_assigns = loader.load_dict(bfres.ResString)
        self.sampler_assigns = loader.load_dict(bfres.ResString)
        self.shader_options = loader.load_dict(bfres.ResString)
