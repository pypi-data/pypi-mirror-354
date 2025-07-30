# pyright: basic
from os import path, remove, makedirs
import sys
from typing import cast
from io import IOBase
from pytest import raises as assert_raises, fixture

from runtime.core.locking import get_shared_lock_path
from runtime.core.locking.handle import Handle
from runtime.locking import LockException, lock_handle, lock_file
from runtime.objects.lifetime import FinalizedError

def test_handle():
    if not path.isdir("tests/testdata"):
        makedirs("tests/testdata")

    filename = path.join("tests", "testdata", f"{__name__}.lock")
    file = open(filename, "w")
    file.write("test")
    pos = file.tell()
    continuation_hit = []

    def fn_continuation(acquired: bool, handle: Handle, fp: IOBase):
        continuation_hit.append(int(acquired))

    try:
        handle1 = Handle(file, filename, __name__, continuation = fn_continuation)
        handle2 = Handle(file, filename, continuation = fn_continuation)

        assert handle1.name == __name__

        with handle1:
            assert file.tell() == pos


            if sys.platform == "win32":
                # concurent locks in same process is prohibited on windows but not linux
                with assert_raises(LockException):
                    handle2.acquire()

                assert 0 in continuation_hit

        assert 1 in continuation_hit

        with assert_raises(FinalizedError):
            handle1.acquire()
        with assert_raises(FinalizedError):
            handle1.release()

        assert handle1.finalized
        assert not handle2.finalized
        assert file.closed

    finally:
        file.close()


def test_lock_file():
    if not path.isdir("tests/testdata"):
        makedirs("tests/testdata")

    filename = path.join("tests", "testdata", f"{__name__}.lock")
    file = open(filename, "w")

    try:
        handle1 = lock_file(filename)
        handle2 = Handle(file, filename)

        if sys.platform == "win32":
            # concurent locks in same process is prohibited on windows but not linux
            with handle1:
                with assert_raises(LockException):
                    handle2.acquire()

        assert not file.closed # lock_file doesn't close file
    finally:
        file.close()

def test_get_shared_lock_path():
    result = get_shared_lock_path("test", elevated=False)
    assert result
    result_elevated = get_shared_lock_path("test", elevated=True)
    assert result_elevated

def test_lock_handle():
    name = __name__
    file_path = get_shared_lock_path(name)

    if path.isfile(file_path):
        remove(file_path)

    handle = cast(Handle, lock_handle(name))
    assert path.abspath(handle.filename) == path.abspath(file_path)

    handle.acquire()

    try:
        with assert_raises(FileExistsError):
            lock_handle(name)
    finally:
        handle.release()
        handle.finalize()

    assert handle.finalized


    handle2 = cast(Handle, lock_handle(name))
    handle2.finalize()