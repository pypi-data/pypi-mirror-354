class TerminateException(Exception):
    """The TerminateException exception is raised when application receives a sigterm or sigint signal.
    The hook_terminate() function is required to set everything up."""

    def __init__(self): # pragma: no cover
        super().__init__("Application requested to terminate")

