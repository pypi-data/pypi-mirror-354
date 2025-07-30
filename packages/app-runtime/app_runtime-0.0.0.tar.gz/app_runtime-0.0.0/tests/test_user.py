# pyright: basic
from os import path, remove
from typing import cast
from pytest import raises as assert_raises, fixture

from runtime.user import get_home, get_roles, get_username, is_elevated, is_admin, is_in_role

def test_get_username():
    username = get_username()
    assert len(username) > 0

def test_get_home():
    username = get_username()
    homedir = get_home()
    assert username.lower() in homedir.lower()
    assert path.isdir(homedir)

def test_get_roles():
    roles = get_roles()
    assert len(roles) > 0

def test_is_elevated():
    result = is_elevated()
    # assert not result # cannot determine expected result in github test dev, so this check cannot safely be done
    assert is_admin == is_elevated

def test_is_in_role():
    roles = get_roles()
    for role in roles:
        assert is_in_role(role)

