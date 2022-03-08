import bfres.core


class AnimCurve(bfres.ResData):
    def __init__(self):
        self.flags = 0
        self.anim_data_offset = 0
        self.start_frame = 0
        self.end_frame = 0
        self.scale = 0
        self.offset = 0
        self.delta = 0
        self.frames = []
        self.keys = []

    def load(self, loader: bfres.core.ResFileLoader):
        self.flags = loader.read_uint16()
        num_key = loader.read_uint16()
        self.anim_data_offset = loader.read_uint32()
        self.start_frame = loader.read_uint32()
        self.end_frame = loader.read_uint32()
        self.scale = loader.read_single()
        self.offset = loader.read_single()
        if loader.res_file.version >= 0x03040000:
            self.delta = loader.read_single()
        frames = loader.load_custom()
