import bfres.core


class BoundingNode(bfres.ResData):
    def __init__(self):
        self.left_child_index: int = 0
        self.right_child_index: int = 0
        self.unknown: int = 0
        self.next_sibling: int = 0
        self.sub_mesh_index: int = 0
        self.sub_mesh_count: int = 0

    def load(self, loader: bfres.core.ResFileLoader):
        self.left_child_index = loader.read_uint16()
        self.right_child_index = loader.read_uint16()
        self.unknown = loader.read_uint16()
        self.next_sibling = loader.read_uint16()
        self.sub_mesh_index = loader.read_uint16()
        self.sub_mesh_count = loader.read_uint16()
