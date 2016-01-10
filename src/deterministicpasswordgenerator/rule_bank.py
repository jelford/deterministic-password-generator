import zipimport

import os

RULEBANK_PATH = 'dpg.rulebank_path'


class RuleSet():
    def __init__(self, module):
        self.module = module

    def generate_password(self, parts):
        return self.module.generate_password(parts)


class RuleBank():
    def __init__(self, base_directory):
        self.base_directory = base_directory
        self.rule_sets = {}
        for fname in os.listdir(base_directory):
            ruleset_name = os.path.splitext(fname)[0]
            importer = zipimport.zipimporter(os.path.join(base_directory, fname))
            module = importer.load_module(ruleset_name)
            self.rule_sets[ruleset_name] = RuleSet(module)

    def get_strategy(self, strategy_name) -> RuleSet:
        return self.rule_sets[strategy_name]


def load_rule_bank(directory: str = None) -> RuleBank:
    base_directory = directory or os.environ.get(RULEBANK_PATH, None) or os.path.join(os.environ.get('HOME'),
                                                                                      '.deterministicpasswordgenerator',
                                                                                      'rulesets')
    return RuleBank(base_directory=directory or base_directory)
