def enable_bit(value: int, index: int) -> int:
    return value | (1 << index)


def disable_bit(value: int, index: int) -> int:
    return value & ~(1 << index)


def get_bit(value: int, index: int) -> bool:
    return value & (1 << index) != 0


def set_bit(value: int, index: int, enable: bool) -> int:
    if enable:
        return enable_bit(value, index)
    else:
        return disable_bit(value, index)


def toggle_bit(value: int, index: int) -> int:
    if get_bit(value, index):
        return disable_bit(value, index)
    else:
        return enable_bit(value, index)


def has_flag(value: int, flag: int) -> bool:
    return (value & flag) != 0
