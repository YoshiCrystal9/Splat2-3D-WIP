from struct import Struct


STRUCTS_CACHE = {}


def get_struct(format: str):
    """
    Returns a `Struct` object for the specified format. If the format exists in the cache, it will use it. Otherwise,
    it will create a new `Struct` object and store it in the cache
    Args:
        format: The format of the values to be packed.

    Returns:
        A `Struct` object for the specified format.
    """
    struct = STRUCTS_CACHE.get(format)
    if not struct:
        struct = Struct(format)
        STRUCTS_CACHE[format] = struct
    return struct
