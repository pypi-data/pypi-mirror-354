# pyright: basic
from os import path, remove

def test_example_1():
    from runtime.application import (
        get_main_module_name, get_application_path, hook_terminate,
        is_interactive, is_python_shell, single_instance,
        SingleInstanceException, TerminateException
    )
    from runtime.user import get_username, is_elevated

    hook_terminate()
    username = get_username()
    module = get_main_module_name()
    app_path = get_application_path()
    interactive = is_interactive()
    is_shell = is_python_shell()

    def output(line: str):
        if interactive:
            print(line)

    try:
        with single_instance():
            try:
                output(f"Hello {'admin ' if is_elevated() else ''}{username}, this is {module} located in {app_path}")
                output(f"I can tell that you're{' not' if not is_shell else ''} running this script in a python shell")
            except TerminateException:
                output(f"Bye {username}")
            except:
                output("An unexpected error ocurred")
    except SingleInstanceException:
        output("Another instance of this application is already running!")


def test_example_2():
    from runtime.locking import lock_file, LockException

    try:
        with lock_file("./lockfile.lock"):
            ...
    except LockException:
        ... # file exists and is already locked

def test_example_3():
    from runtime.locking import lock_handle, LockException

    try:
        with lock_handle("lock"):
            ...
    except LockException:
        ... # a handle exists and is already locked


def test_example_4():
    from io import IOBase
    from os import remove
    from runtime.locking import Handle, LockException

    def fn_continuation(acquired: bool, handle: Handle, fp: IOBase):
        remove(handle.filename)

    try:
        filename = "tests/lockfile.lock"
        file = open(filename, "w")
        with Handle(file, filename, "Lock", continuation = fn_continuation):
            ...

        assert not path.isfile(filename)

    except LockException:
        ... # a handle exists and is already locked


def test_example_5():
    from runtime.objects.lifetime import Finalizable, FinalizedError

    try:
        class Test(Finalizable):
            _is_finalized = False

            def __finalize__(self) -> None:
                self._is_finalized = True

        instance = Test()
        ...
        instance.finalize()

        assert instance.finalized

    except FinalizedError:
        ... # instance has been finalized


