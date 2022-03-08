import bfres.core


class ResString(bfres.ResData):
    def __init__(self):
        self.value = None
        self.encoding = None

    def load(self, loader: bfres.core.ResFileLoader):
        self.value = loader.read_string_0(self.encoding or loader.encoding)
