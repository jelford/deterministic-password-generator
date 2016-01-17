import zipfile
from getpass import getpass

import os
import stat
import tempfile
from os import path

from .crypto import encrypt


def compile_ruleset(ruleset_path, ruleset_encryption_password=None, output_path=None):
    output_path = output_path or os.getcwd()
    ruleset_encryption_password = ruleset_encryption_password or getpass('Password (used to encrypt compiled ruleset):')

    ruleset_name = path.basename(ruleset_path)

    with tempfile.SpooledTemporaryFile() as output_ruleset:
        with zipfile.PyZipFile(output_ruleset, mode='w') as ruleset:
            ruleset.writepy(pathname=ruleset_path)

        output_ruleset.seek(0)
        encrypted_output = encrypt(output_ruleset.read(), key=ruleset_encryption_password)

    compiled_ruleset_output_path = path.join(output_path, '{ruleset}.dpgr'.format(ruleset=ruleset_name))
    with open(compiled_ruleset_output_path, 'wb') as output:
        os.chmod(compiled_ruleset_output_path, stat.S_IREAD)
        output.write(encrypted_output)
