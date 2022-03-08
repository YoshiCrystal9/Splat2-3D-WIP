import io

from binaryio.binaryreader import BinaryReader
from binaryio.binarywriter import BinaryWriter


def _get_context(base, **kwargs):
    class BinaryFileContext(base):
        def __init__(self, file_path: str, mode: str, buffer_size: int, encoding: str, endianness: str):
            self._mode = mode
            self._buffer_size = buffer_size
            self._encoding = encoding
            self._endianness = endianness
            self._file_path = file_path

        def __enter__(self):
            self._file = open(self._file_path, self._mode)
            super().__init__(self._file.raw, self._buffer_size, self._encoding, self._endianness)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()

    return BinaryFileContext(**kwargs)


def open_binary(file_path: str, mode: str = 'rb', buffer_size: int = io.DEFAULT_BUFFER_SIZE,
                encoding: str = 'utf-8', endianness: str = ""):
    """
    Opens a context manager for reading or writing a binary file using the `BinaryReader` or `BinaryWriter` class.
    Args:
        file_path: The file path for the binary file.
        mode: The mode in which to open it. This should be 'rb' or 'wb' for reading or writing respectively.
        buffer_size: The buffer size for the file.
        encoding: The encoding to use for strings in the file.
        endianness: The endian format for the file.

    Returns:
        A context manager for reading or writing a binary file using the `BinaryReader` or `BinaryWriter` class.
    """
    assert mode in ('rb', 'wb'), "Invalid mode: only 'rb' and 'wb' are valid."
    base = BinaryWriter if mode == 'wb' else BinaryReader
    return _get_context(base,
                        file_path=file_path, mode=mode, buffer_size=buffer_size,
                        encoding=encoding, endianness=endianness
                        )
