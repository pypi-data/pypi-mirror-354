class SingleInstanceException(Exception):
    """The SingleInstanceException exception is raised when another instance of the application is already running.
    The single_instance() function is required to set everything up."""

    def __init__(self): # pragma: no cover
        super().__init__("Another instance of application is already running...!")

