import sys
import itertools

import pytest

from mashup.core import CHARSETS, DEFAULT_LENGTH, DEFAULT_CHARSETS, generate
from mashup.parser import parse


names = [cs['longname'] for cs in CHARSETS]
flags = itertools.chain.from_iterable(itertools.combinations(names, i) for i in range(1, len(names) + 1))


@pytest.mark.parametrize("flag,charset", [(cs['longname'], cs['charset']) for cs in CHARSETS])
def test_include_one_flag_only(monkeypatch, flag, charset):
    monkeypatch.setattr(sys, "argv", ["main.py"] + [f"--{flag}", "16", "--do-not-copy"])

    args = parse(CHARSETS)
    sequence = generate(args)

    assert len(sequence) == 16
    assert all(c in charset for c in sequence), f"Found characters outside {flag} charset"


@pytest.mark.parametrize("flags", flags)
def test_charset_flag_combinations(monkeypatch, flags):
    monkeypatch.setattr(sys, "argv", ["main.py"] + [f"--{flag}" for flag in flags] + ["16", "--do-not-copy"])

    args = parse(CHARSETS)
    sequence = generate(args)

    pool = "".join(cs['charset'] for cs in CHARSETS if cs['longname'] in flags)

    assert len(sequence) == 16
    assert pool, "Charset pool is empty"
    assert all(c in pool for c in sequence), f"Invalid char in combo {flags}"


def test_charset_flag_custom(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py"] + ["--custom", "q", "16", "--do-not-copy"])

    args = parse(CHARSETS)
    sequence = generate(args)

    assert len(sequence) == 16
    assert all(c == "q" for c in sequence), "Found characters outside q"


def test_charset_flag_empty(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py"])

    args = parse(CHARSETS)
    sequence = generate(args)

    pool = "".join(cs['charset'] for cs in CHARSETS if cs['longname'] in DEFAULT_CHARSETS)

    assert len(sequence) == DEFAULT_LENGTH
    assert pool, "Charset pool is empty"
    assert all(c in pool for c in sequence), f"Invalid char in combo {DEFAULT_CHARSETS}"
