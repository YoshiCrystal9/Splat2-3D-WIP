from typing import Generic, Iterator, List, MutableMapping, Tuple, TypeVar, Union

import bfres
import bfres.core

T = TypeVar('T')
Key = Union[int, str, T]


class ResDict(bfres.ResData, MutableMapping[str, T]):
    def __init__(self, value_type: type):
        self._nodes: List[ResDictNode[T]] = []
        self._value_type = value_type

    def __contains__(self, item):
        for node in self._nodes[1:]:
            if node.key == item:
                return True
        return False

    def __delitem__(self, key: Union[int, str]) -> None:
        if isinstance(key, int):
            del self._nodes[key + 1]
        elif isinstance(key, str):
            for i, node in enumerate(self._nodes[1:]):
                if node.key == key:
                    del self._nodes[i]
            raise KeyError(f"{key} does not exist in {self}.")
        else:
            raise TypeError(f"{key} is not of a valid key type.")

    def __getitem__(self, key: Union[int, str]) -> T:
        if isinstance(key, int):
            return self._nodes[key + 1].value
        elif isinstance(key, str):
            for node in self._nodes[1:]:
                if node.key == key:
                    return node.value
            raise KeyError(f"{key} does not exist in {self}.")
        else:
            raise TypeError(f"{key} is not of a valid key type.")

    def __iter__(self) -> Iterator[str]:
        for node in self._nodes[1:]:
            yield node.key

    def __len__(self) -> int:
        return len(self._nodes) - 1

    def __setitem__(self, key: Union[int, str], value: T) -> None:
        if isinstance(key, int):
            self._nodes[key + 1].value = value
        elif isinstance(key, str):
            for node in self._nodes[1:]:
                if node.key == key:
                    node.value = value
            self._nodes.append(ResDictNode(key, value))
        else:
            raise TypeError(f"{key} is not of a valid key type.")

    def load(self, loader: bfres.core.ResFileLoader):
        # Read the header.
        size: int = loader.read_uint32()
        num_nodes: int = loader.read_int32()  # Excludes root node.
        # Read the nodes including the root node.
        self._nodes: List[ResDictNode] = []
        for i in range(num_nodes + 1):
            node = ResDictNode()
            node.load(loader, self._value_type)
            self._nodes.append(node)

    def remove(self, value: T):
        for node in self._nodes[1:]:
            if node.value == value:
                self._nodes.remove(node)


class ResDictNode(Generic[T]):
    def __init__(self, key: str = "", value: T = None):
        self.reference: int = 0xFFFFFFFF
        self.idx_left: int = 0
        self.idx_right: int = 0
        self.key: str = key
        self.value: T = value

    def load(self, loader: bfres.core.ResFileLoader, value_type: type):
        self.reference = loader.read_uint32()
        self.idx_left = loader.read_uint16()
        self.idx_right = loader.read_uint16()
        self.key = loader.load_string()
        self.value = loader.load(value_type)
