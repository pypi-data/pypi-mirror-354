from mashup.core import CHARSETS, copy, generate
from mashup.parser import parse


def main():
    args = parse(CHARSETS)
    sequence = generate(args)
    (copy(sequence), print(sequence)) if not args.do_not_copy else print(sequence)


if __name__ == '__main__':
    main()
