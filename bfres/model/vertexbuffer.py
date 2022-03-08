from typing import List
import io

import bfres
import bfres.core


class VertexBuffer(bfres.ResData):
    def __init__(self):
        self.vertex_skin_count: int = 0
        self.attributes: bfres.ResDict[bfres.VertexAttrib] = bfres.ResDict(bfres.VertexAttrib)
        self.buffers: List[bfres.Buffer] = []

    def load(self, loader: bfres.core.ResFileLoader):
        loader.check_signature("FVTX")
        num_vertex_attrib = loader.read_byte()
        num_buffer = loader.read_byte()
        idx = loader.read_uint16()
        vertex_count = loader.read_uint32()
        self.vertex_skin_count = loader.read_byte()
        loader.seek(3, io.SEEK_CUR)
        ofs_vertex_attrib_list = loader.read_offset()  # Only load dict.
        self.attributes = loader.load_dict(bfres.VertexAttrib)
        self.buffers = loader.load_list(bfres.Buffer, num_buffer)
        user_pointer = loader.read_uint32()
