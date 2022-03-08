import abc
import bfres.core


class ResData:
    @abc.abstractmethod
    def load(self, loader: bfres.core.ResFileLoader):
        pass
