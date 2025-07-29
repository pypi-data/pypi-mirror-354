import argparse

from keyvomit.core import DEFAULT_LENGTH


def parse(charsets: list[dict[str, str, str, str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='keyvomit',

        description=(
            "mash together a sequence of characters so unhinged, even regex will flinch.\n"
            "You can mix individual flags like --lower or --digits, smash them together like -ludsp,\n"
            "or go full wildcard with --custom and see what happens.\n"
        ),

        epilog=(
            "examples:\n"
            "   keyvomit --lower --upper\n"
            "       → Generate a 16-character sequence using just lowercase and uppercase letters.\n\n"
            "   keyvomit -luds\n"
            "       → Combined shorthand: lowercase, uppercase, digits, safe symbols.\n\n"
            "   keyvomit --custom 'abc123!?🐍' 24\n"
            "       → 24 characters from your personal font of bad decisions.\n\n"
            "defaults:\n"
            "   if you pass no flags or charsets, keyvomit defaults to: \n"
            "   lowercase, uppercase, digits, and safe symbols.\n"
            "   length defaults to 16 characters.\n\n"
            "may your sequences be strong and your intent unclear.\n"
        ),

        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'length',
        type=int,
        nargs='?',
        default=DEFAULT_LENGTH,
        help=f"Sequence length (default: {DEFAULT_LENGTH} — long enough to annoy but short enough to memorize badly)."
    )

    for chset in charsets:
        parser.add_argument(
            *((f"-{chset.get('shortname')}", ) if chset.get('shortname') else ()) + (f"--{chset.get('longname')}", ),
            action='store_true',
            help=chset.get('description')
        )

    parser.add_argument(
        '-c', '--custom',
        type=str,
        help="Use your own characters (for when nothing else feels right)."
    )

    parser.add_argument(
        '-n', '--do-not-copy',
        action='store_true',
        help="Don't copy the result to clipboard (useful for minimalists and masochists)."
    )

    return parser.parse_args()
