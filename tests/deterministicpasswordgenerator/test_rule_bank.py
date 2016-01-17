import os
import pytest
import tempfile

import deterministicpasswordgenerator.rule_bank as rule_bank
from deterministicpasswordgenerator.compile import compile_ruleset


def compile_folder_and_install_as_ruleset(rulebank_base_directory, ruleset_name):
    path_to_ruleset = os.path.abspath(os.path.join(os.path.dirname(__file__), ruleset_name))
    compile_ruleset(
            ruleset_path=path_to_ruleset,
            ruleset_encryption_password='test-key',
            output_path=rulebank_base_directory)


@pytest.yield_fixture(params=('mock_ruleset_simple', 'mock_ruleset_multifile'))
def installed_ruleset(tempdir: tempfile.TemporaryDirectory, request):
    compile_folder_and_install_as_ruleset(tempdir.name, request.param)
    yield request.param


def test_loads_rule_bank_from_rulebank_path(tempdir, installed_ruleset):
    loaded = rule_bank.load_rule_bank(directory=tempdir.name, encryption_key='test-key')

    strategy = loaded.get_strategy(installed_ruleset)
    assert type(strategy) == rule_bank.RuleSet
    result = strategy.generate_password(['a', 'b', 'c'])
    assert result == 'abc'


if __name__ == '__main__':
    import pytest

    pytest.main(__file__)
