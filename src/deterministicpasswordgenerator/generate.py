from .rule_bank import load_rule_bank


class PasswordGenerator():
    def __init__(self, rule_bank):
        self.rule_bank = rule_bank

    def generate(self, ruleset_name, parts):
        ruleset_name = self.rule_bank.get_strategy(ruleset_name)
        return ruleset_name.generate(parts)


def generate_password(ruleset_name, parts):
    PasswordGenerator(load_rule_bank()).generate(ruleset_name, parts)
