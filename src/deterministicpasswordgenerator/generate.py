from getpass import getpass

from .rule_bank import load_rule_bank


class PasswordGenerator():
    def __init__(self, rule_bank):
        self.rule_bank = rule_bank

    def generate(self, ruleset_name, parts):
        ruleset = self.rule_bank.get_strategy(ruleset_name)
        return ruleset.generate_password(parts)


def generate_password(ruleset_name, parts, encryption_key=None):
    encryption_key = encryption_key or getpass('Password (to decrypt ruleset):')
    print(PasswordGenerator(load_rule_bank(encryption_key=encryption_key)).generate(ruleset_name, parts))
