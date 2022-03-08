import io

from struct import Struct
from typing import Tuple

from binaryio.seektask import SeekTask
from binaryio.structs import get_struct


class BinaryReader(io.BufferedReader):
    """
    Reads values from a binary file.
    """
    def __init__(self, raw, buffer_size=io.DEFAULT_BUFFER_SIZE, encoding: str = "utf-8", endianness: str = ""):
        """
        Args:
            raw: The buffer for the binary file.
            buffer_size: The maximum size of the buffer before flushing.
            encoding: The default encoding to use when writing strings.
            endianness: The endian format in which bytes are arranged.
        """
        super().__init__(raw, buffer_size=buffer_size)
        self._default_encoding = encoding
        self._endianness = endianness

    def __repr__(self):
        return f"{self.__class__} tell()={self.tell()}"

    def _read_value(self, fmt: str):
        """
        Reads a single value of a specified format from the stream.
        Args:
            fmt: The format string for the value to be read from the stream.

        Returns:
            The value read from the stream.
        """
        struct = get_struct(f"{self._endianness}{fmt}")
        return struct.unpack(self.read(struct.size))[0]

    def _read_values(self, fmt: str, count: int) -> tuple:
        """
        Reads a series of values of a specified format from the stream.
        Args:
            fmt: The format string for the values to be read from the stream.
            count: The number of values to be read from the stream.

        Returns:
            A `tuple` containing the values read from the stream.
        """
        full_format = f"{self._endianness}{count}{fmt}"
        struct = Struct(full_format)
        return struct.unpack(self.read(struct.size))

    def align(self, alignment: int) -> None:
        """
        Seeks to the nearest byte (earlier than current position) which is a multiple of `alignment`.
        Args:
            alignment: The number whose multiple to seek to.
        """
        self.seek(-self.tell() % alignment, io.SEEK_CUR)

    def read_byte(self) -> int:
        """
        Reads the next byte.
        Returns:
            The value of the next byte.
        """
        return self.read(1)[0]

    def read_bytes(self, count: int) -> bytes:
        """
        Reads the next `count` bytes.
        Args:
            count: The number of bytes to read.

        Returns:
            The values of the next `count` bytes.
        """
        return self.read(count)

    def read_int16(self) -> int:
        """
        Reads a 16-bit integer from the current position.
        Returns:
            The 16-bit integer that is read.
        """
        return self._read_value("h")

    def read_int16s(self, count: int) -> Tuple[int]:
        """
        Reads `count` consecutive 16-bit integers from the current position.
        Args:
            count: The number of 16-bit integers to read.

        Returns:
            The `count` consecutive 16-bit integers that are read.
        """
        return self._read_values("h", count)

    def read_int32(self) -> int:
        """
        Reads a 32-bit integer from the current position.
        Returns:
            The 32-bit integer that is read.
        """
        return self._read_value("i")

    def read_int32s(self, count: int) -> Tuple[int]:
        """
        Reads `count` consecutive 32-bit integers from the current position.
        Args:
            count: The number of 32-bit integers to read.

        Returns:
            The `count` consecutive 32-bit integers that are read.
        """
        return self._read_values("i", count)

    def read_sbyte(self) -> int:
        """
        Reads the next signed char.
        Returns:
            The next signed chars.
        """
        return self._read_value("b")

    def read_sbytes(self, count: int) -> Tuple[int]:
        """
        Reads the next `count` signed chars
        Args:
            count: The number of signed chars to read.

        Returns:
            The next `count` signed chars.
        """
        return self._read_values("b", count)

    def read_single(self) -> float:
        """
        Reads a single-precision floating point number from the current position.
        Returns:
            The single-precision loating point number that is read.
        """
        return self._read_value("f")

    def read_singles(self, count: int) -> Tuple[float]:
        """
        Reads `count` consecutive single-precision floating point numbers from the current position
        Args:
            count: The number of single-precision floating point numbers to read.

        Returns:
            The `count` consecutive single-precision floating point integers that are read.

        """
        return self._read_values("f", count)

    def read_0_string(self, encoding: str = None) -> str:
        """
        Reads a null-terminated string from the current position.
        Args:
            encoding: The encoding of the string. The default encoding for the class will be used if no encoding is
                      specified.

        Returns:
            The null-terminated string that is read.
        """
        # This will not work for strings with differently sized characters depending on their code.
        char_size = len("a".encode(encoding or self._default_encoding))
        str_bytes = bytearray()
        read_bytes = bytearray(self.read(char_size))
        while any(read_bytes):
            str_bytes.extend(read_bytes)
            read_bytes = bytearray(self.read(char_size))
        return str_bytes.decode(encoding or self._default_encoding)

    def read_raw_string(self, length: int, encoding: str = None) -> str:
        """
        Reads a string of known length from the current position.
        Args:
            length: The number of bytes used to represent the string.
            encoding: The encoding of the string. The default encoding for the class will be used if no encoding is
                      specified.

        Returns:
            The string of length specified that is read.
        """
        return self.read(length).decode(encoding or self._default_encoding)

    def read_uint16(self) -> int:
        """
        Reads an unsigned 16-bit integer from the current position.
        Returns:
            The unsigned 16-bit integer that is read.
        """
        return self._read_value("H")

    def read_uint16s(self, count: int) -> Tuple[int]:
        """
        Reads `count` consecutive unsigned 16-bit integers from the current position.
        Args:
            count: The number of unsigned 16-bit integers to read.

        Returns:
            The `count` consecutive unsigned 16-bit integers that are read.
        """
        return self._read_values("H", count)

    def read_uint32(self) -> int:
        """
        Reads an unsigned 32-bit integer from the current position.
        Returns:
            The unsigned 32-bit integer that is read.
        """
        return self._read_value("I")

    def read_uint32s(self, count: int) -> Tuple[int]:
        """
        Reads `count` consecutive unsigned 32-bit integers from the current position.
        Args:
            count: The number of unsigned 32-bit integers to read.

        Returns:
            The `count` consecutive unsigned 32-bit integers that are read.
        """
        return self._read_values("I", count)

    def read_int64(self) -> int:
        """
        Reads a 64-bit integer from the current position.
        Returns:
            The 64-bit integer that is read.
        """
        return self._read_value("q")

    def read_int64s(self, count: int) -> Tuple[int]:
        """
        Reads `count` consecutive 64-bit integers from the current position.
        Args:
            count: The number of 64-bit integers to read.

        Returns:
            The `count` consecutive 64-bit integers that are read.
        """
        return self._read_values("q", count)

    def read_uint64(self) -> int:
        """
        Reads an unsigned 64-bit integer from the current position.
        Returns:
            The unsigned 64-bit integer that is read.
        """
        return self._read_value("Q")

    def read_uint64s(self, count: int) -> Tuple[int]:
        """
        Reads `count` consecutive unsigned 64-bit integers from the current position.
        Args:
            count: The number of unsigned 64-bit integers to read.

        Returns:
            The `count` consecutive unsigned 64-bit integers that are read.
        """
        return self._read_values("Q", count)

    def read_double(self) -> float:
        """
        Reads a double-precision floating point number from the current position.
        Returns:
            The double-precision loating point number that is read.
        """
        return self._read_value("d")

    def read_doubles(self, count: int) -> Tuple[float]:
        """
        Reads `count` consecutive double-precision floating point numbers from the current position
        Args:
            count: The number of double-precision floating point numbers to read.

        Returns:
            The `count` consecutive double-precision floating point integers that are read.
        """
        return self._read_values("d", count)

    def read_length_prefixed_string(self, encoding: str = None) -> str:
        """
        Reads a length-prefixed string from the current position.
        Args:
            encoding: The encoding of the string. The default encoding for the class will be used if no encoding is
                      specified.

        Returns:
            The string that is read.
        """
        n_bytes = self.read_int16()
        return self.read_raw_string(n_bytes, encoding)

    def temporary_seek(self, offset: int = 0, whence=io.SEEK_SET) -> SeekTask:
        """
        Returns a `SeekTask` object which can be used to temporarily seek to other positions and return to the
        current position when the task is exited.
        Args:
            offset: The number of bytes to initially seek.
            whence: The position from which to seek the `offset` bytes.

        Returns:
            A `SeekTask` object which remembers the current position and returns to it when the task is exited.
        """
        return SeekTask(self, offset, whence)
