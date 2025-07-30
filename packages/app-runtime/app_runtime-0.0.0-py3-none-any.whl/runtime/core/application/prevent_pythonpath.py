from os import path, environ
from sys import argv, path as syspath

def prevent_pythonpath(suppress_info: bool = True) -> None: # pragma: no cover
    """Prevents paths in development from entering the sys.path,
    either because the current working directory contains a python init script,
    or because one or more paths are injected via the PYTHONPATH environment variable.

    Example:
    Using application X1 on the same machine where new development is being done,
    calling 'X1' inside the development folder would normally launch the version under development
    and not the installed obe

    To use it, call it from the root __init__ script.

    Args:
        suppress_info (bool, optional): Supress printing the information to stdout. Defaults to True.
    """


    cwd = path.abspath(path.dirname(argv[0]))

    if cwd in syspath:
        if not suppress_info:
            print(f"Removing {cwd} from sys.path")
        syspath.remove(cwd)

    if pythonpath := environ.get("PYTHONPATH", ""):
        pythonpath = path.abspath(pythonpath)

        if pythonpath in syspath:
            if not suppress_info:
                print(f"Removing {pythonpath} from sys.path")
            syspath.remove(pythonpath)

