import builtins
import sys

from mashup.core import copy


def test_copy_with_pyperclip(monkeypatch):
    clipboard = {}

    class FakePyperclip:
        @staticmethod
        def copy(value):
            clipboard["value"] = value

    monkeypatch.setitem(sys.modules, "pyperclip", FakePyperclip)

    copy("hello world")

    assert clipboard["value"] == "hello world"


def test_copy_without_pyperclip(monkeypatch, capsys):
    if "pyperclip" in sys.modules:
        del sys.modules["pyperclip"]

    original_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "pyperclip":
            raise ModuleNotFoundError

        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    copy("doesn’t matter")
    captured = capsys.readouterr()

    assert "[Error] 'pyperclip' module is required" in captured.out
