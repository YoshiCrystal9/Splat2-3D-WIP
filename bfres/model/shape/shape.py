from typing import List
import enum

import bfres
import bfres.core


class ShapeFlags(enum.IntFlag):
    NONE = 0
    HAS_VERTEX_BUFFER = 1 << 1


class Shape(bfres.ResData):
    _SIGNATURE = "FSHP"

    def __init__(self):
        self.name: str = ""
        self.flags: bfres.ShapeFlags = ShapeFlags.NONE
        self.material_index: int = -1
        self.bone_index: int = -1
        self.vertex_buffer_index: int = -1
        self.vertex_skin_cunt: int = -1
        self.target_attrib_count: int = -1
        self.radius: float = 0
        self.vertex_buffer: bfres.VertexBuffer = None
        self.meshes: List[bfres.Mesh] = []
        self.skin_bone_indices: List[int] = []
        self.key_shapes: bfres.ResDict[bfres.KeyShape] = bfres.ResDict(bfres.KeyShape)
        self.sub_mesh_bounding_nodes: List[bfres.BoundingNode] = []
        self.sub_mesh_boundings: List[bfres.Bounding] = []
        self.sub_mesh_bounding_indices: List[int] = []

    def load(self, loader: bfres.core.ResFileLoader):
        loader.check_signature(self._SIGNATURE)
        self.name = loader.load_string()
        self.flags = ShapeFlags(loader.read_uint32())
        idx = loader.read_uint16()
        self.material_index = loader.read_uint16()
        self.bone_index = loader.read_uint16()
        self.vertex_buffer_index = loader.read_uint16()
        num_skin_bone_index = loader.read_uint16()
        self.vertex_skin_cunt = loader.read_byte()
        num_mesh = loader.read_byte()
        num_key_shape = loader.read_byte()
        self.target_attrib_count = loader.read_byte()
        num_sub_mesh_bounding_nodes = loader.read_uint16()  # Padding in engine
        self.radius = loader.read_single()
        self.vertex_buffer = loader.load(bfres.VertexBuffer)
        self.meshes = loader.load_list(bfres.Mesh, num_mesh)
        self.skin_bone_indices = loader.load_custom(lambda l: l.read_uint16s(num_skin_bone_index))
        self.key_shapes = loader.load_dict(bfres.KeyShape)
        if num_sub_mesh_bounding_nodes:
            self.sub_mesh_bounding_nodes = loader.load_list(bfres.BoundingNode, num_sub_mesh_bounding_nodes)
            self.sub_mesh_boundings = loader.load_custom(lambda l: l.read_boundings(num_sub_mesh_bounding_nodes))
            self.sub_mesh_bounding_indices = loader.load_custom(lambda l: l.read_uint16s(num_sub_mesh_bounding_nodes))
        else:
            # Compute the count differently if the node count was padding.
            self.sub_mesh_boundings = loader.load_custom(lambda l: l.read_boundings(len(self.meshes[0].sub_meshes)) + 1)
        user_pointer = loader.read_uint32()
