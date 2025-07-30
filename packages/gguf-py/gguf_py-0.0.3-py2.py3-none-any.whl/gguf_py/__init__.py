# !/usr/bin/env python3

__version__ = '0.0.3'

def __init__():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand", help="choose a subcommand:")
    subparsers.add_parser('a', help='[a] assembler')
    subparsers.add_parser('d', help='[d] decomposer')
    args = parser.parse_args()
    if args.subcommand == 'a':
        from gguf_connector import f
    if args.subcommand == 'd':
        from pig_gguf import d