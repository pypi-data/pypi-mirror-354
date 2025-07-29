import argparse
from os import urandom as random


CHARSETS = [
    {
        'shortname': 'l',
        'longname': 'lower',
        'description': "Lowercase letters (a–z) — for when you're feeling chill and unthreatening.",
        'charset': 'abcdefghijklmnopqrstuvwxyz',
    },

    {
        'shortname': 'u',
        'longname': 'upper',
        'description': "Uppercase letters (A–Z) — BECAUSE SOMETIMES YOU GOTTA YELL.",
        'charset': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    },

    {
        'shortname': 'd',
        'longname': 'digits',
        'description': "Digits (0–9) — numbers you’ll forget instantly but insist on including.",
        'charset': '0123456789',
    },

    {
        'shortname': 'x',
        'longname': 'hexdigits',
        'description': "Hexadecimal digits (0–9, A–F) — for people who think in RGB and bleed machine code.",
        'charset': '0123456789ABCDEF',
    },

    {
        'shortname': 's',
        'longname': 'symbols',
        'description': "Safe symbols curated to avoid breaking your shell, config, or brain.",
        'charset': '!@#$%^&*()-_=+[]{}',
    },

    {
        'shortname': 'p',
        'longname': 'punctuation',
        'description': "All punctuation — full ASCII chaos, includes things like '~' or '\\' and other fragile demons.",
        'charset': r"#$%&'()*+,-./:;<=>?@[\]^_`{|}~" + '"',
    },
]

DEFAULT_LENGTH = 32
DEFAULT_CHARSETS = [
    'lower',
    'upper',
    'digits',
    'symbols',
]


def copy(sequence: str) -> None:
    try:
        import pyperclip
        pyperclip.copy(sequence)

    except ModuleNotFoundError:
        print("[Error] 'pyperclip' module is required to copy to a clipboard. Try 'pip install pyperclip' to fix this")


def generate(args: argparse.Namespace) -> str:
    flags = [cs.get('longname') for cs in CHARSETS if getattr(args, cs.get('longname'))] or DEFAULT_CHARSETS
    pool = (list(set(c for c in args.custom)) if args.custom else
            list(set([c for cs in [cs.get('charset') for cs in CHARSETS if cs.get('longname') in flags] for c in cs])))

    return "".join(pool[byte % len(pool)] for byte in random(args.length * 2))[:args.length]
