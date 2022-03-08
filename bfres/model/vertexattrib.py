import io

import bfres.core
import bfres.gx2


class VertexAttrib(bfres.ResData):
    def __init__(self):
        self.name: str = ""
        self.buffer_index: int = 0
        self.offset: int = 0
        self.format: bfres.gx2.GX2AttribFormat = 0

    def load(self, loader: bfres.core.ResFileLoader):
        self.name = loader.load_string()
        self.buffer_index = loader.read_byte()
        loader.seek(1, io.SEEK_CUR)
        self.offset = loader.read_uint16()
        self.format = bfres.gx2.GX2AttribFormat(loader.read_uint32())
