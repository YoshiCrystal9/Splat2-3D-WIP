import bfres.core


class SubMesh(bfres.ResData):
    def __init__(self):
        self.offset: int = 0
        self.count: int = 0

    def load(self, loader: bfres.core.ResFileLoader):
        self.offset = loader.read_uint32()
        self.count = loader.read_uint32()
