import io

import bfres.core
import bfres.gx2


class Sampler(bfres.ResData):
    def __init__(self):
        self.tex_sampler: bfres.gx2.TexSampler = bfres.gx2.TexSampler()
        self.name: str = ""

    def load(self, loader: bfres.core.ResFileLoader):
        self.tex_sampler = bfres.gx2.TexSampler(loader.read_uint32s(3))
        handle = loader.read_uint32()
        self.name = loader.load_string()
        idx = loader.read_byte()
        loader.seek(3, io.SEEK_CUR)
