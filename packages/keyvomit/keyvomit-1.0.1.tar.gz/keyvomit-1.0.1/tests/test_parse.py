import sys
import pytest

from keyvomit.core import CHARSETS, DEFAULT_LENGTH
from keyvomit.parser import parse


@pytest.mark.parametrize("arglist,expected", [
    ([], {'length': DEFAULT_LENGTH, 'do_not_copy': False}),
    (["32"], {'length': 32}),
    (["--lower", "24"], {'lower': True, 'length': 24}),
    (["-u", "--digits"], {'upper': True, 'digits': True}),
    (["--custom", "abc123!?"], {'custom': "abc123!?"}),
    (["--do-not-copy"], {'do_not_copy': True}),
])
def test_parse_args(monkeypatch, arglist, expected):
    monkeypatch.setattr(sys, "argv", ["mashup.py"] + arglist)

    args = parse(CHARSETS)

    for key, val in expected.items():
        assert getattr(args, key) == val


@pytest.mark.parametrize("flag", [cs['longname'] for cs in CHARSETS])
def test_all_flags(monkeypatch, flag):
    monkeypatch.setattr(sys, "argv", ["mashup.py", f"--{flag}"])

    args = parse(CHARSETS)

    assert getattr(args, flag) is True
