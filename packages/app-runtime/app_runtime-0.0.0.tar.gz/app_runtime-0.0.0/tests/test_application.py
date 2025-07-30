# pyright: basic
from os import path, remove
import sys
from typing import cast
from pytest import raises as assert_raises, fixture
from importlib.metadata import version

from runtime.core.application import SINGLE_INSTANCE_FILENAME
from runtime.core.locking import get_shared_lock_path, lock_file
from runtime.core.locking.handle import Handle

from runtime.locking import LockException
from runtime.application import (
    single_instance, is_interactive, is_python_shell, get_main_module_name,
    get_application_path, get_main_module, get_installalled_apps_path, get_all_packages
)

def test_single_instance():
    file_path = get_shared_lock_path(SINGLE_INSTANCE_FILENAME)

    if path.isfile(file_path):
        remove(file_path)

    handle = cast(Handle, single_instance())
    assert path.isfile(handle.filename)
    handle.acquire()
    handle.release()
    assert not path.isfile(handle.filename)

    # handle1 = cast(Handle, single_instance())
    # handle2 = cast(Handle, lock_file(handle1.filename))

    # handle2.acquire()
    # self.assertRaises(LockException, handle1.acquire)
    # x=0

    # handle1.finalize()


def test_is_interactive():
    result = is_interactive()
    assert not result

def test_is_python_shell():
    result = is_python_shell()
    assert not result

def test_get_application_path():
    result = get_application_path()
    assert result == getattr(sys.modules["__main__"], "__file__")

def test_get_installed_apps_path():
    result = get_installalled_apps_path(elevated=False)

    if sys.platform == "win32":
        assert path.isdir(path.dirname(result)) # check parent dir as the nested 'Programs' folder might not exist on windows servers
    else:
        assert path.isdir(path.dirname(result)) # check parent dir as the nested '.local' folder might not exist on linux servers


    result = get_installalled_apps_path(ensure_exists=True, elevated=False)
    assert path.isdir(result)

    result = get_installalled_apps_path(elevated=True)
    assert path.isdir(result) # check parent dir as the nested 'Programs' folder might not exist on windows servers

def test_get_main_module():
    result = get_main_module()
    assert result == sys.modules["__main__"]

def test_get_main_module_name():
    result = get_main_module_name()
    assert result # result may equal __main__ when tested

def test_get_all_packages():
    result = get_all_packages()
    assert result

