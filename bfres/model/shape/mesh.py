import io
from typing import List

import bfres.core
import bfres.gx2


class Mesh(bfres.ResData):
    def __init__(self):
        self.primitive_type: bfres.gx2.GX2PrimitiveType = 0
        self.index_format: bfres.gx2.GX2IndexFormat = 0
        self.sub_meshes: List[bfres.SubMesh] = []
        self.index_buffer: bfres.Buffer = None
        self.first_vertex: int = 0

    def load(self, loader: bfres.core.ResFileLoader):
        self.primitive_type = bfres.gx2.GX2PrimitiveType(loader.read_uint32())
        self.index_format = bfres.gx2.GX2IndexFormat(loader.read_uint32())
        index_count = loader.read_uint32()
        num_sub_mesh = loader.read_uint16()
        loader.seek(2, io.SEEK_CUR)
        self.sub_meshes = loader.load_list(bfres.SubMesh, num_sub_mesh)
        self.index_buffer = loader.load(bfres.Buffer)
        self.first_vertex = loader.read_uint32()
