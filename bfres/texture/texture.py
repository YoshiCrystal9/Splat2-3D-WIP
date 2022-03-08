import io

import bfres.core
import bfres.gx2


class Texture(bfres.ResData):
    def __init__(self):
        self.dim = bfres.gx2.GX2SurfaceDim.DIM_1D
        self.width = 0
        self.height = 0
        self.depth = 0
        self.mip_count = 0
        self.format = bfres.gx2.GX2SurfaceFormat.INVALID
        self.aa_mode = bfres.gx2.GX2AAMode.MODE_1X
        self.use = bfres.gx2.GX2SurfaceUse.TEXTURE
        self.tile_mode = bfres.gx2.GX2TileMode.DEFAULT
        self.swizzle = 0
        self.alignment = 0
        self.pitch = 0
        self.mip_offsets = 0
        self.view_mip_first = 0
        self.view_mip_count = 0
        self.view_slice_first = 0
        self.view_slice_count = 0
        self.comp_sel_r = bfres.gx2.GX2CompSel.CHANNEL_R
        self.comp_sel_g = bfres.gx2.GX2CompSel.CHANNEL_G
        self.comp_sel_b = bfres.gx2.GX2CompSel.CHANNEL_B
        self.comp_sel_a = bfres.gx2.GX2CompSel.CHANNEL_A
        self.regs = ()
        self.array_length = 0
        self.name = None
        self.path = None
        self.data = []
        self.mip_data = []
        self.user_data = bfres.ResDict(bfres.UserData)

    def load(self, loader: bfres.core.ResFileLoader):
        loader.check_signature("FTEX")
        self.dim = bfres.gx2.GX2SurfaceDim(loader.read_uint32())
        self.width = loader.read_uint32()
        self.height = loader.read_uint32()
        self.depth = loader.read_uint32()
        self.mip_count = loader.read_uint32()
        self.format = bfres.gx2.GX2SurfaceFormat(loader.read_uint32())
        self.aa_mode = bfres.gx2.GX2AAMode(loader.read_uint32())
        self.use = bfres.gx2.GX2SurfaceUse(loader.read_uint32())
        siz_data = loader.read_uint32()
        image_pointer = loader.read_uint32()
        siz_map_data = loader.read_uint32()
        mip_pointer = loader.read_uint32()
        self.tile_mode = bfres.gx2.GX2TileMode(loader.read_uint32())
        self.swizzle = loader.read_uint32()
        self.alignment = loader.read_uint32()
        self.pitch = loader.read_uint32()
        self.mip_offsets = loader.read_uint32s(13)
        self.view_mip_first = loader.read_uint32()
        self.view_mip_count = loader.read_uint32()
        self.view_slice_first = loader.read_uint32()
        self.view_slice_count = loader.read_uint32()
        self.comp_sel_r = bfres.gx2.GX2CompSel(loader.read_byte())
        self.comp_sel_g = bfres.gx2.GX2CompSel(loader.read_byte())
        self.comp_sel_b = bfres.gx2.GX2CompSel(loader.read_byte())
        self.comp_sel_a = bfres.gx2.GX2CompSel(loader.read_byte())
        self.regs = loader.read_uint32s(5)
        handle = loader.read_uint32()
        self.array_length = loader.read_uint32()  # Possibly just a byte.
        self.name = loader.load_string()
        self.path = loader.load_string()
        self.data = loader.load_custom(lambda l: l.read_bytes(siz_data))
        self.mip_data = loader.load_custom(lambda l: l.read_bytes(siz_map_data))
        self.user_data = loader.load_dict(bfres.UserData)
        num_user_data = loader.read_uint16()
        loader.seek(2, io.SEEK_CUR)
