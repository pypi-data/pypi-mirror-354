# compatability classes, variables and functions for the msvcrt module on windows

LK_UNLCK: int = 0
LK_LOCK: int = 1
LK_NBLCK: int = 2
LK_RLCK: int = 3
LK_NBRLCK: int = 4

def locking(fd: int, mode: int, nbytes: int, /) -> None: # pragma: no cover
    raise NotImplementedError