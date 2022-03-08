import io

from struct import Struct
from typing import Iterable

from binaryio.structs import get_struct


class BinaryWriter(io.BufferedWriter):
    def __init__(self, raw, buffer_size: int=io.DEFAULT_BUFFER_SIZE, encoding: str = "utf-8", endianness: str = ""):
        super().__init__(raw, buffer_size=buffer_size)
        self._default_encoding = encoding
        self._endianness = endianness

    def _write_value(self, fmt: str, value):
        """
        Writes a single value of a specified format to the stream.
        Args:
            fmt: The format string for the value to be written to the stream.
            value: The value to write to the stream.
        """
        struct = get_struct(f"{self._endianness}{fmt}")
        self.write(struct.pack(value))

    def _write_values(self, fmt: str, values: Iterable):
        """
        Writes an iterable of values of the specified format to the stream.
        Args:
            fmt: The format of the values to be written to the stream.
            values: The iterable of values to be written to the stream.
        """
        # This does not use _get_struct because the length of `values` may change frequently so the cache
        # would not be effective.
        full_format = f"{self._endianness}{len(values)}{fmt}"
        self.write(Struct(full_format).pack(*values))

    def align(self, alignment: int):
        """
        Seeks to the nearest byte (earlier than current position) which is a multiple of `alignment`.
        Args:
            alignment: The number whose multiple to seek to.
        """
        self.seek(-self.tell() % alignment, io.SEEK_CUR)

    def write_0_string(self, value: str, encoding: str = None):
        """
        Writes a null-terminated string at the current position.
        Args:
            encoding: The encoding of the string. The default encoding for the class will be used if no encoding is
                      specified.
        """
        self.write_raw_string(value, encoding)
        self.write_byte(0)

    def write_byte(self, value: int):
        """
        Writes a byte at the current position.
        Args:
            value: The value of the byte to write.
        """
        self._write_value("B", value)

    def write_bytes(self, value: bytes):
        """
        Writes consecutive bytes at the current position.
        Args:
            value: The bytes to write.
        """
        self.write(value)

    def write_int32(self, value: int):
        """
        Writes a 32-bit integer at the current position.
        Args:
            value: The 32-bit integer to write.
        """
        self._write_value("i", value)

    def write_int32s(self, value: Iterable[int]):
        """
        Writes consecutive 32-bit integers at the current position.
        Args:
            value: The 32-bit integers to write.
        """
        self._write_values("i", value)

    def write_sbyte(self, value: int):
        """
        Writes a signed char at the current position.
        Args:
            value: The value of the signed char to write.
        """
        self._write_value("b", value)

    def write_sbytes(self, value: Iterable[int]):
        """
        Writes consecutive signed chars at the current position.
        Args:
            value: The signed chars to write.
        """
        self._write_values("b", value)

    def write_single(self, value: float):
        """
        Writes a single-precision floating point number at the current position.
        Args:
            value: The single-precision floating point number to write.
        """
        self._write_value("f", value)

    def write_singles(self, value: Iterable[float]):
        """
        Writes consecutive single-precision floating point numbers at the current position.
        Args:
            value: The single-precision floating point numbers to write.
        """
        self._write_values("f", value)

    def write_int16(self, value: int):
        """
        Writes a 16-bit integer at the current position.
        Args:
            value: The 16-bit integer to write.
        """
        self._write_value("h", value)

    def write_int16s(self, value: Iterable[int]):
        """
        Writes consecutive 16-bit integers at the current position.
        Args:
            value: The 16-bit integers to write.
        """
        self._write_values("h", value)

    def write_uint16(self, value: int):
        """
        Writes an unsigned 16-bit integer at the current position.
        Args:
            value: The unsigned 16-bit integer to write.
        """
        self._write_value("H", value)

    def write_uint16s(self, value: Iterable[int]):
        """
        Writes consecutive unsigned 16-bit integers at the current position.
        Args:
            value: The unsigned 16-bit integers to write.
        """
        self._write_values("H", value)

    def write_uint32(self, value: int):
        """
        Writes an unsigned 32-bit integer at the current position.
        Args:
            value: The unsigned 32-bit integer to write.
        """
        self._write_value("I", value)

    def write_uint32s(self, value: Iterable[int]):
        """
        Writes consecutive unsigned 32-bit integers at the current position.
        Args:
            value: The unsigned 32-bit integers to write.
        """
        self._write_values("I", value)

    def write_int64(self, value: int):
        """
        Writes a 64-bit integer at the current position.
        Args:
            value: The 64-bit integer to write.
        """
        self._write_value("q", value)

    def write_int64s(self, value: Iterable[int]):
        """
        Writes consecutive 64-bit integers at the current position.
        Args:
            value: The 64-bit integers to write.
        """
        self._write_values("q", value)

    def write_uint64(self, value: int):
        """
        Writes an unsigned 64-bit integer at the current position.
        Args:
            value: The unsigned 64-bit integer to write.
        """
        self._write_value("Q", value)

    def write_uint64s(self, value: Iterable[int]):
        """
        Writes consecutive unsigned 64-bit integers at the current position.
        Args:
            value: The unsigned 64-bit integers to write.
        """
        self._write_values("Q", value)

    def write_raw_string(self, value: str, encoding: str = None):
        """
        Writes a string at the current position.
        Args:
            value: The string to write.
            encoding: The encoding of the string. The default encoding for the class will be used if no encoding is
                      specified.
        """
        self.write(bytes(value, encoding=encoding or self._default_encoding))

    def write_double(self, value: float):
        """
        Writes a double-precision floating point number at the current position.
        Args:
            value: The double-precision floating point number to write.
        """
        self._write_value("d", value)

    def write_doubles(self, value: Iterable[float]):
        """
        Writes consecutive double-precision floating point numbers at the current position.
        Args:
            value: The double-precision floating point numbers to write.
        """
        self._write_values("d", value)

    def write_length_prefixed_string(self, value: str, encoding: str = None):
        """
        Writes a length-prefixed string at the current position.
        Args:
            value: The string to write.
            encoding: The encoding of the string. The default encoding for the class will be used if no encoding is
                      specified.
        """
        bytes_to_write = bytes(value, encoding=encoding or self._default_encoding)
        self.write_int16(len(bytes_to_write))
        self.write(bytes_to_write)
