from typing import Any
from abc import ABC, abstractmethod
from weakref import finalize

from runtime.core.objects.lifetime.finalized_error import FinalizedError

class Finalizable(ABC):
    """Base class for implementation of the Finalizable pattern.
    When instances of a derived class are garbage collected, finalization takes place automatically.
    """
    __slots__ = [ "__weakref__", "__finalizer", "__finalizing" ]

    def __new__(cls, *args: Any, **kwargs: Any):

        def fn_finalize():
            instance.__finalizing = True
            instance.__finalize__() # pyright: ignore[reportAbstractUsage]
            instance.__finalizing = False

        instance = super().__new__(cls)
        instance.__finalizer = finalize(instance, fn_finalize)
        instance.__finalizing = False

        return instance

    @property
    def finalized(self) -> bool:
        """Indicates if object has been finalized or not."""
        return not self.__finalizer.alive

    @property
    def finalizing(self) -> bool:
        """Indicates if object is in the process of finalizing or not."""
        return self.__finalizing

    def finalize(self) -> None:
        """Initiates the finalization process manually."""
        if not self.__finalizer.alive:
            raise FinalizedError

        self.__finalizer()

    @abstractmethod
    def __finalize__(self) -> None:
        """This function is invoked when finalization process is initiated."""
        ... # pragma: no cover
