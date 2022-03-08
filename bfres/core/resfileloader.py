from typing import Dict

import io

import bfres
import bfres.core
import binaryio


class ResFileLoader(binaryio.BinaryReader):
    def __init__(self, res_file, raw):
        """
        Initializes a new instance loading data into the given res_file from the specified bytes-like raw object.
        :param res_file: The ResFile instance to load data into.
        :param raw: The bytes-like object to read data from.
        """
        super().__init__(raw)
        self.endianness: str = ">"  # Big-endian
        self.res_file: bfres.ResFile = res_file
        self._data_map: Dict[int, bfres.ResData] = {}

    def execute(self):
        """
        Starts deserializing the data from the res_file root.
        """
        self.res_file.load(self)

    def check_signature(self, valid_signature: str):
        """
        Reads a BFRES signature consisting of 4 ASCII characters encoded as an uint32 and checks for validity.
        :param valid_signature: A valid signature.
        """
        signature = self.read_string_raw(len(valid_signature))
        if signature != valid_signature:
            raise bfres.ResException(f"Invalid signature, expected {valid_signature} but got {signature}.")

    def load(self, value_type: type):
        """
        Reads and returns an instance of the value_type from the following offset or returns None if the read offset is
        0.
        :param value_type: The type of the instance to read.
        :return: The instance or None.
        """
        offset = self.read_offset()
        if not offset:
            return None
        with self.temporary_seek(offset, io.SEEK_SET):
            return self._read_res_data(value_type)

    def load_custom(self, callback, offset: int = None):
        """
        Reads and returns an instance of arbitrary type from the following offset with the given callback or returns
        None if the read offset is 0.
        :param callback: The callback to read the instance data with.
        :param offset: The optional offset to use instead of reading a following one.
        :return: The data instance or None.
        """
        offset = offset or self.read_offset()
        if not offset:
            return None
        with self.temporary_seek(offset, io.SEEK_SET):
            return callback(self)

    def load_dict(self, value_type: type):
        """
        Reads and returns a ResDict instance with elements of the given value_type from the following offset or returns
        an empty instance if the read offset is 0.
        :param value_type: The type of the elements.
        :return: The ResDict instance.
        """
        offset = self.read_offset()
        resdict = bfres.ResDict(value_type)
        if not offset:
            return resdict
        with self.temporary_seek(offset, io.SEEK_SET):
            resdict.load(self)
            return resdict

    def load_list(self, value_type: type, count: int, offset: int = None):
        items = []
        offset = offset or self.read_offset()
        if not offset or not count:
            return items
        # Seek to the list start and read it.
        with self.temporary_seek(offset, io.SEEK_SET):
            for i in range(count):
                items.append(self._read_res_data(value_type))
        return items

    def load_string(self, encoding: str = None):
        """
        Reads and returns a str instance from the following offset or None if the read offset is 0.
        :return: The read text.
        """
        offset = self.read_offset()
        if not offset:
            return None
        with self.temporary_seek(offset, io.SEEK_SET):
            return self.read_string_0(encoding or self.encoding)

    def load_strings(self, count: int, encoding: str = None):
        """
        Reads and returns str instances from the following offsets.
        :param count: The number of instances to read.
        :param encoding: The optional encoding of the texts.
        :return: The read texts.
        """
        offsets = self.read_offsets(count)
        encoding = encoding or self.encoding
        names = []
        with self.temporary_seek():
            for offset in offsets:
                if not offset:
                    continue
                self.seek(offset, io.SEEK_SET)
                names.append(self.read_string_0(encoding))
        return names

    def read_bounding(self):
        bounding = bfres.Bounding()
        bounding.center = self.read_vector3f()
        bounding.extent = self.read_vector3f()
        return bounding

    def read_boundings(self, count: int):
        values = []
        for i in range(count):
            values.append(self.read_matrix3x4())
        return values

    def read_matrix3x4(self):
        return (self.read_single(), self.read_single(), self.read_single(), self.read_single()), \
               (self.read_single(), self.read_single(), self.read_single(), self.read_single()), \
               (self.read_single(), self.read_single(), self.read_single(), self.read_single()),

    def read_matrix3x4s(self, count: int):
        values = []
        for i in range(count):
            values.append(self.read_matrix3x4())
        return values

    def read_offset(self):
        """
        Reads a BFRES offset which is relative to itself, and returns the absolute address.
        :return: The absolute address of the offset.
        """
        offset = self.read_int32()
        return self.tell() - 4 + offset if offset else 0

    def read_offsets(self, count: int):
        """
        Reads BFRES offsets which are relative to themselves, and returns the absolute addresses.
        :param count: The number of offsets to read.
        :return: The absolute addresses of the offsets.
        """
        values = []
        for i in range(count):
            values.append(self.read_offset())
        return values

    def read_vector3f(self):
        return self.read_single(), self.read_single(), self.read_single()

    def read_vector4f(self):
        return self.read_single(), self.read_single(), self.read_single(), self.read_single()

    def _read_res_data(self, value_type: type):
        offset = self.tell()
        # Same data can be referenced multiple times. Load it in any case to move in the stream, needed for lists.
        instance = value_type()
        instance.load(self)
        # If possible, return an instance already representing the data.
        existing_instance = self._data_map.get(offset)
        if existing_instance:
            return existing_instance
        else:
            self._data_map[offset] = instance
            return instance
