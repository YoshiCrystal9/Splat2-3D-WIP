import bfres
import bfres.core


class Buffer(bfres.ResData):
    def __init__(self):
        self._size = 0
        self._num_buffering = 0
        self.stride = 0
        self.data = None

    def load(self, loader: bfres.core.ResFileLoader):
        data_pointer = loader.read_uint32()
        self._size = loader.read_uint32()
        handle = loader.read_uint32()
        self.stride = loader.read_uint16()
        self._num_buffering = loader.read_uint16()
        context_pointer = loader.read_uint32()
        self.data = loader.load_custom(self._load_data)

    def _load_data(self, loader: bfres.core.ResFileLoader):
        data = []
        for i in range(self._num_buffering):
            data.append(loader.read_bytes(self._size))
        return data
