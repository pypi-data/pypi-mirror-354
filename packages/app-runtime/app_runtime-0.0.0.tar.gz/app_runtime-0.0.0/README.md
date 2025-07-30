[![Test](https://github.com/apmadsen/app-runtime/actions/workflows/python-test.yml/badge.svg)](https://github.com/apmadsen/app-runtime/actions/workflows/python-test.yml)
[![Coverage](https://github.com/apmadsen/app-runtime/actions/workflows/python-test-coverage.yml/badge.svg)](https://github.com/apmadsen/app-runtime/actions/workflows/python-test-coverage.yml)
[![Stable Version](https://img.shields.io/pypi/v/app-runtime?label=stable&sort=semver&color=blue)](https://github.com/apmadsen/app-runtime/releases)
![Pre-release Version](https://img.shields.io/github/v/release/apmadsen/app-runtime?label=pre-release&include_prereleases&sort=semver&color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/app-runtime)
[![PyPI Downloads](https://static.pepy.tech/badge/app-runtime/week)](https://pepy.tech/projects/app-runtime)

# app-runtime
This project provides cross-platform tools for handling the context of a Python application, including getting system, user and application info.

## Example

```python
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

```
## Full documentation

[Go to documentation](https://github.com/apmadsen/app-runtime/blob/main/docs/documentation.md)