from typing import List

import bfres.core


class KeyShape(bfres.ResData):
    def __init__(self):
        self.target_attrib_indices: List[int] = []
        self.target_attrib_index_offsets: List[int] = []

    def load(self, loader: bfres.core.ResFileLoader):
        self.target_attrib_indices = loader.read_bytes(20)
        self.target_attrib_index_offsets = loader.read_bytes(4)
