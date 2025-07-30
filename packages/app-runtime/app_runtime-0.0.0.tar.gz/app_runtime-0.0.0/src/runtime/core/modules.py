from typing import overload
from os import path
from types import ModuleType
from sys import path as syspath
from importlib.util import spec_from_file_location, module_from_spec

@overload
def load_module(module_path: str) -> ModuleType:
    """Load module given its full path.

    Args:
        module_path (str): The module path.

    Returns:
        ModuleType: The loaded module.
    """
    ...
@overload
def load_module(module_path: str, module_name: str) -> ModuleType:
    """Load module by name from root path.

    Args:
        module_path (str): The module root path.

    Returns:
        ModuleType: The loaded module.
    """
    ...
def load_module(module_path: str, module_name: str | None = None) -> ModuleType:
    if module_name:
        if not path.isdir(module_path):
            raise FileNotFoundError(module_path)

        try:
            if not module_path in syspath:
                syspath.insert(0, module_path)

            module = __import__(module_name, fromlist=module_name.split(".", maxsplit = 1)[0])
            return module
        except ModuleNotFoundError:
            raise
        # except KeyError:
        #     raise ModuleNotFoundError(module_name)

    else:
        if not path.isfile(module_path):
            raise FileNotFoundError(module_path)

        spec = spec_from_file_location(path.basename(module_path).split(".")[0], module_path)

        if not spec: # pragma: no cover
            raise Exception(f"Unable to load {module_path}")

        module = module_from_spec(spec)
        spec.loader.exec_module(module) # pyright: ignore[reportOptionalMemberAccess]
        return module

