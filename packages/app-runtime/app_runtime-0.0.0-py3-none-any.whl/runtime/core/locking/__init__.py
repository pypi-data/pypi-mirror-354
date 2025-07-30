import sys
from os import path, remove, makedirs
from typing import ContextManager, Any
from io import IOBase
from platformdirs import site_runtime_dir, user_runtime_dir

from runtime.core.user import USER_ELEVATED
from runtime.core.locking.handle import Handle
from runtime.core.locking.log import log

def lock_file(file_path: str) -> ContextManager[Any]:
    """Returns a Handle object for specified file_path."""
    log.debug(f"Creating a handle for {file_path}")
    return Handle(open(file_path, 'w'), file_path)

def lock_handle(name: str) -> ContextManager[Any]:
    """Returns a named Handle object in the common system path for shared locks."""
    file_path = get_shared_lock_path(name)

    if ( dir := path.dirname(file_path) ) and not path.isdir(dir): # pragma: no cover
        log.info(f"Creating nonexisting dir {dir}...")
        makedirs(dir)

    if path.isfile(file_path):
        log.error(f"Cannot create a handle for {file_path} because it already exists")
        raise FileExistsError(file_path)

    def cleanup(acquired: bool, handle: Handle, fp: IOBase):
        if acquired:
            log.debug(f"Cleaning up handle by disposing of {handle.filename}")
            remove(handle.filename)

    return Handle(open(file_path, 'w'), file_path, name, continuation = cleanup)

def get_shared_lock_path(name: str, *, elevated: bool = USER_ELEVATED) -> str:
    """Returns the common system path for locks.

    Args:
        name (str): The name of the lock.
        elevated (bool, optional): Specifies it user is running under elevated privileges (is admin/sudo). Defaults to USER_ELEVATED.
    """

    command = path.basename(sys.argv[0].split(" ", maxsplit = 1)[0])

    if elevated:
        file_path = path.join(site_runtime_dir(), f"{command}_{name}.lock")
    else:
        file_path = path.join(user_runtime_dir(), f"{command}_{name}.lock")

    return file_path