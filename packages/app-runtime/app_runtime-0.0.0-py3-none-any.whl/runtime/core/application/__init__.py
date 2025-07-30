import sys
from os import isatty, path, getenv, makedirs
from types import ModuleType
from typing import ContextManager, Any
from platformdirs import user_data_dir
from importlib.metadata import Distribution, distributions

from runtime.core.locking.lock_exception import LockException
from runtime.core.application.log import log
from runtime.core.application.single_instance_exception import SingleInstanceException
from runtime.core.locking import lock_handle
from runtime.core.user import get_home, USER_ELEVATED

MAIN_MODULE = sys.modules["__main__"]
SINGLE_INSTANCE_FILENAME = "singleinstance"

def get_main_module() -> ModuleType:
    """Returns the main module."""
    return MAIN_MODULE

def get_main_module_name() -> str:
    """Returns the real name of the main module."""
    module_name = getattr(MAIN_MODULE, "__name__")

    if module_name == "__main__" and hasattr(MAIN_MODULE, "__package__"):
        if pkg := getattr(MAIN_MODULE, "__package__"):
            return pkg

    if module_name == "__main__" and hasattr(MAIN_MODULE, "__file__"): # pragma: no cover
        file_path = getattr(MAIN_MODULE, "__file__")
        file_name = path.splitext(path.basename(file_path))[0]
        if file_name.lower() != "__main__":
            return file_name

    return module_name # pragma: no cover

def get_all_packages() -> dict[str, Distribution]:
    """Returns all installed packages."""
    return {
        dist.name: dist
        for dist in distributions()
    }

def get_application_path() -> str:
    """Returns the path of the main module. If running in a Python shell, the path of the executable is returned."""
    if hasattr(MAIN_MODULE, "__file__"):
        return getattr(MAIN_MODULE, "__file__")
    else: # pragma: no cover
        return sys.executable

def is_interactive() -> bool:
    """Indicates if application is running inside a terminal or not."""
    try:
        return isatty(sys.stdout.fileno())
    except: # pragma: no cover
        return False

def is_python_shell() -> bool:
    """Indicates if application is running inside a python shell or not."""
    return not hasattr(MAIN_MODULE, "__file__")

def single_instance() -> ContextManager[Any]:
    """Returns a SingleInstance context, which ensures that application is only running in one instance."""
    try:
        return lock_handle(SINGLE_INSTANCE_FILENAME)
    except LockException as ex: # pragma: no cover
        log.error("Another instance of application is apparently running")
        raise SingleInstanceException from ex

def get_installalled_apps_path(*, ensure_exists: bool = False, elevated: bool = USER_ELEVATED) -> str: # pragma: no cover
    """Gets the default path for installed user applications.

    Args:
        ensure_exists (bool, optional): Specifies whether or not creation of nonexistent folder should be attempted. Applies to elevated user context only.
        elevated (bool, optional): Specifies it user is running under elevated privileges (is admin/sudo). Defaults to USER_ELEVATED.
    """
    if elevated:
        if sys.platform == "win32":
            if result := (getenv("PROGRAMFILES") or
                          getenv("PROGRAMFILES(X86)") or
                          getenv("PROGRAMW6432")):

                return path.abspath(result)
        elif sys.platform == "linux":
            for result in ("/usr/local/bin", "/usr/local/sbin"):
                if path.isdir(result):
                    return "/usr/local/bin"

        log.error(f"Unable to locate a path for installed apps ({sys.platform})")
    else:
        if sys.platform == "win32":
            result = path.abspath(path.join(user_data_dir(), "Programs"))
            if result and ensure_exists and not path.isdir(result):
                log.info(f"Creating nonexisting dir {result}...")
                makedirs(result)
            return result
        elif sys.platform == "linux":
            if ( home := get_home() ):
                result = path.join(home, ".local")
                if result and ensure_exists and not path.isdir(result):
                    log.info(f"Creating nonexisting dir {result}...")
                    makedirs(result)
                return result

        log.error(f"Unable to locate a path for installed apps ({sys.platform})")
    raise FileNotFoundError

