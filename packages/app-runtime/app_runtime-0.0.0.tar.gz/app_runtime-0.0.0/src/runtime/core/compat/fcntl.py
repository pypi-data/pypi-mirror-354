# compatability classes, variables and functions for the fcntl module on linux

from io import IOBase

LOCK_SH: int = 1
LOCK_EX: int = 2
LOCK_NB: int = 4
LOCK_UN: int = 8
LOCK_MAND: int = 32
LOCK_READ: int = 64
LOCK_WRITE: int = 128
LOCK_RW: int = 192

def lockf(fd: IOBase, cmd: int, len: int = 0, start: int = 0, whence: int = 0, /) -> None: # pragma: no cover
    raise NotImplementedError