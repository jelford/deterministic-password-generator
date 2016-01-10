import zipfile

import os
from os import path


def compile_ruleset(ruleset_path, output_path=None):
    output_path = output_path or os.getcwd()

    ruleset_name = path.basename(ruleset_path)

    compiled_ruleset = path.join(output_path, '{ruleset}.dpgr'.format(ruleset=ruleset_name))

    with zipfile.PyZipFile(compiled_ruleset, mode='w') as ruleset:
        ruleset.writepy(pathname=ruleset_path)
