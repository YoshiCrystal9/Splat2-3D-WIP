import io


class SeekTask:
    """
    A context manager class which remembers the current position of the stream and seeks back to this position
    after exiting.
    """
    def __init__(self, raw, offset: int, whence):
        self.raw = raw
        self.offset = offset
        self.whence = whence

    def __enter__(self):
        self.previous_pos = self.raw.tell()
        self.raw.seek(self.offset, self.whence)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.raw.seek(self.previous_pos, io.SEEK_SET)
