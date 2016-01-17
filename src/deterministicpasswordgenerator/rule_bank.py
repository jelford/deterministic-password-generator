import zipimport

import os
import tempfile

from .crypto import decrypt

RULEBANK_PATH = 'dpg.rulebank_path'


class RuleSet():
    def __init__(self, module):
        self.module = module

    def generate_password(self, parts):
        return self.module.generate_password(parts)


class RuleBank():
    def __init__(self, base_directory, encryption_key):
        self.base_directory = base_directory
        self.rule_sets = {}
        for fname in os.listdir(base_directory):
            ruleset_name = os.path.splitext(fname)[0]
            file = os.path.join(base_directory, fname)

            with open(file, 'rb') as ruleset_file:
                decrypted = decrypt(ruleset_file.read(), key=encryption_key)

            module = self.load_module_from_decrypted_data(decrypted, ruleset_name)

            self.rule_sets[ruleset_name] = RuleSet(module)

    def load_module_from_decrypted_data(self, decrypted, ruleset_name):
        handle, path = tempfile.mkstemp()
        try:
            os.write(handle, decrypted)
            os.close(handle)
            importer = zipimport.zipimporter(path)
            module = importer.load_module(ruleset_name)
        finally:
            os.remove(path)
        return module

    def get_strategy(self, strategy_name) -> RuleSet:
        return self.rule_sets[strategy_name]


def load_rule_bank(encryption_key, directory: str = None) -> RuleBank:
    base_directory = directory or _installed_rulebank_path()
    return RuleBank(base_directory=base_directory, encryption_key=encryption_key)


def install_ruleset(path):
    import shutil
    rulebank_path = _installed_rulebank_path()
    try:
        os.makedirs(rulebank_path)
    except FileExistsError:
        pass

    shutil.copyfile(path, os.path.join(rulebank_path, os.path.basename(path)))


def _installed_rulebank_path() -> str:
    return os.environ.get(RULEBANK_PATH, None) or os.path.join(os.environ.get('HOME'),
                                                               '.deterministicpasswordgenerator', 'rulesets')
