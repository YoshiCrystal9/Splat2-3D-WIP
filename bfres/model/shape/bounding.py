from typing import Tuple


class Bounding:
    def __init__(self):
        self.center: Tuple[float, float, float] = (0, 0, 0)
        self.extent: Tuple[float, float, float] = (0, 0, 0)
