import bfres
import bfres.core


class TextureRef(bfres.ResData):
    def __init__(self):
        self.name = None
        self.texture = None

    def load(self, loader: bfres.core.ResFileLoader):
        self.name = loader.load_string()
        self.texture = loader.load(bfres.Texture)
