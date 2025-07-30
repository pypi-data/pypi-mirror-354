# pyright: basic
from pytest import raises as assert_raises, fixture

from runtime.modules import load_module

def test_load_module():
    with assert_raises(FileNotFoundError):
        some_module = load_module("tests/nonexistingdir/some_module.py")

    some_module = load_module("tests/some_module.py")
    assert getattr(some_module, "test") == "test"

def test_load_module_by_name():
    with assert_raises(FileNotFoundError):
        some_module = load_module("tests/nonexistingdir", "some_module")

    with assert_raises(ModuleNotFoundError):
        some_module = load_module("tests", "nonexisting_module")

    some_module = load_module("tests", "some_module")
    assert getattr(some_module, "test") == "test"
