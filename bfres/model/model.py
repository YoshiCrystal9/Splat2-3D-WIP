from typing import List

import bfres
import bfres.core


class Model(bfres.ResData):
    """
    Represents an FMDL subfile in a ResFile, storing model vertex data, skeletons and used materials.
    """

    _SIGNATURE = "FMDL"

    def __init__(self):
        self.name: str = ""
        self.path: str = ""
        self.skeleton: bfres.Skeleton = None
        self.vertex_buffers: List[bfres.VertexBuffer] = None
        self.shapes: List[bfres.Shape] = None
        self.materials: List[bfres.Material] = None
        self.user_data: bfres.ResDict[bfres.UserData] = None

    def load(self, loader: bfres.core.ResFileLoader):
        loader.check_signature(self._SIGNATURE)
        self.name = loader.load_string()
        self.path = loader.load_string()
        self.skeleton = loader.load(bfres.Skeleton)
        ofs_vertex_buffer_list = loader.read_offset()
        self.shapes = loader.load_dict(bfres.Shape)
        self.materials = loader.load_dict(bfres.Material)
        self.user_data = loader.load_dict(bfres.UserData)
        num_vertex_buffer = loader.read_uint16()
        num_shape = loader.read_uint16()
        num_material = loader.read_uint16()
        num_user_data = loader.read_uint16()
        total_vertex_count = loader.read_uint32()
        user_pointer = loader.read_uint32()
        self.vertex_buffers = loader.load_list(bfres.VertexBuffer, num_vertex_buffer, ofs_vertex_buffer_list)
