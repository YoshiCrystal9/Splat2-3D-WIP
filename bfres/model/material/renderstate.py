from typing import Tuple

import enum
import bfres.core
import bfres.gx2


class RenderStateFlagsMode(enum.IntEnum):
    CUSTOM = 0
    OPAQUE = 1
    ALPHA_MASK = 2
    TRANSLUCENT = 3


class RenderStateFlagsBlendMode(enum.IntEnum):
    NONE = 0
    COLOR = 1
    LOGICAL = 2


class RenderState(bfres.ResData):
    _FLAGS_MASK_MODE = 0b00000000_00000000_00000000_00000011
    _FLAGS_MASK_BLEND_MODE = 0b00000000_00000000_00000000_00110000

    def __init__(self):
        self._flags: int = 0
        self.polygon_control: bfres.gx2.PolygonControl = bfres.gx2.PolygonControl()
        self.depth_control: bfres.gx2.DepthControl = bfres.gx2.DepthControl()
        self.alpha_control: bfres.gx2.AlphaControl = bfres.gx2.AlphaControl()
        self.color_control: bfres.gx2.ColorControl = bfres.gx2.ColorControl()
        self.blend_control: bfres.gx2.BlendControl = bfres.gx2.BlendControl()
        self.blend_color: Tuple[float, float, float, float] = (0, 0, 0, 0)

    @property
    def flags_mode(self) -> RenderStateFlagsMode:
        return RenderStateFlagsMode(self._flags & self._FLAGS_MASK_MODE)

    @flags_mode.setter
    def flags_mode(self, value: RenderStateFlagsMode):
        self._flags &= ~self._FLAGS_MASK_MODE | value

    @property
    def flags_blend_mode(self) -> RenderStateFlagsBlendMode:
        return RenderStateFlagsBlendMode(self._flags & self._FLAGS_MASK_BLEND_MODE)

    @flags_blend_mode.setter
    def flags_blend_mode(self, value: RenderStateFlagsBlendMode):
        self._flags &= ~self._FLAGS_MASK_BLEND_MODE | value

    def load(self, loader: bfres.core.ResFileLoader):
        self._flags = loader.read_uint32()
        self.polygon_control = bfres.gx2.PolygonControl(loader.read_uint32())
        self.depth_control = bfres.gx2.DepthControl(loader.read_uint32())
        self.alpha_control = bfres.gx2.AlphaControl(loader.read_uint32(), loader.read_single())
        self.color_control = bfres.gx2.ColorControl(loader.read_uint32())
        self.blend_control = bfres.gx2.BlendControl(loader.read_uint32(), loader.read_uint32())
        self.blend_color = loader.read_vector4f()
