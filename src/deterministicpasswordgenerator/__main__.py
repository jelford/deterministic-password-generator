import argparse
import sys

from .compile import compile_ruleset
from .generate import generate_password
from .rule_bank import install_ruleset


def parse_args(sys_args) -> (argparse.ArgumentParser, argparse.Namespace):
    parser = argparse.ArgumentParser(description='Work with password rulesets')
    subparsers = parser.add_subparsers()

    generate_password_parser = subparsers.add_parser('generate_password')
    generate_password_parser.add_argument('ruleset_name', type=str,
                                          help='Which ruleset should be used to generate your password?')
    generate_password_parser.add_argument('parts', type=str, nargs=argparse.REMAINDER)
    generate_password_parser.set_defaults(func=generate_password)

    compile_ruleset_parser = subparsers.add_parser('compile_ruleset')
    compile_ruleset_parser.add_argument('ruleset_path', type=str, help='Where are your rules currently stored?')
    compile_ruleset_parser.add_argument('--output_path', type=argparse.FileType('w'), help='Where to put your file?',
                                        required=False)
    compile_ruleset_parser.set_defaults(func=compile_ruleset)

    install_ruleset_parser = subparsers.add_parser('install_ruleset')
    install_ruleset_parser.add_argument('path', type=str, help='Path to your compiled rulset')
    install_ruleset_parser.set_defaults(func=install_ruleset)

    return parser, parser.parse_args(sys_args)


def main():
    parser, args = parse_args(sys.argv[1:])
    args_to_pass = vars(args)
    try:
        to_call = args_to_pass.pop('func')
    except KeyError:
        parser.print_usage()
        sys.exit(-1)
    to_call(**args_to_pass)


if __name__ == '__main__':
    main()
