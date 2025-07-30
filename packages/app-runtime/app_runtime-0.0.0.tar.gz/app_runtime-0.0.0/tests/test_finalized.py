# pyright: basic
from os import path
from pytest import raises as assert_raises, fixture

from runtime.objects.lifetime import Finalizable, FinalizedError


def test_finalizable():
    class Test(Finalizable):
        _is_finalized = False

        def __finalize__(self) -> None:
            self._is_finalized = True

    t = Test()

    assert not t.finalized
    assert not t._is_finalized

    t.finalize()

    assert t.finalized
    assert t._is_finalized

    with assert_raises(FinalizedError):
        t.finalize()

