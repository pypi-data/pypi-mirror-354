class LockException(Exception): # pragma: no cover
    """The LockException exception is raised when a handle is already locked."""
    def __init__(self, handle: str):
        super().__init__(f"Handle {handle} is already locked by another instance of this application...!")
