import argparse
import sys

from .compile import compile_ruleset
from .generate import generate_password


def parse_args(sys_args):
    parser = argparse.ArgumentParser(description='Work with password rulesets')
    subparsers = parser.add_subparsers()

    generate_password_parser = subparsers.add_parser('generate_password')
    generate_password_parser.add_argument('ruleset_name', type=str,
                                          help='Which ruleset should be used to generate your password?')
    generate_password_parser.add_argument('parts', type=str, nargs=argparse.REMAINDER)
    generate_password_parser.set_defaults(func=generate_password)

    install_ruleset_parser = subparsers.add_parser('compile_ruleset')
    install_ruleset_parser.add_argument('ruleset_path', type=str, help='Where are your rules currently stored?')
    install_ruleset_parser.add_argument('--output_path', type=argparse.FileType('w'), help='Where to put your file?',
                                        required=False)
    install_ruleset_parser.set_defaults(func=compile_ruleset)

    return parser.parse_args(sys_args)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    args_to_pass = vars(args)
    to_call = args_to_pass.pop('func')
    to_call(**args_to_pass)
