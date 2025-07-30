from signal import signal, SIGTERM, SIGINT
from threading import current_thread, main_thread
from typing import Any

from runtime.core.application.terminate_exception import TerminateException
from runtime.core.application.log import log

def hook_terminate() -> None: # pragma: no cover
    """Hooks up interrupt and terminate handlers, which throws a TerminateException when signaled."""
    if current_thread() is main_thread():
        def handler(signum: int, frame: Any) -> None:
            raise TerminateException()

        signal(SIGTERM, handler)
        signal(SIGINT, handler)
    else:
        log.error("hook_terminate() is not called from the main thread")
        raise Exception("hook_terminate() must be called from the main thread!")
