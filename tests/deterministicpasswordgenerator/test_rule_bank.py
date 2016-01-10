import zipfile

import os
import pytest
import tempfile

import deterministicpasswordgenerator.rule_bank as rule_bank


def compile_folder_and_install_as_ruleset(rulebank_base_directory, path_to_ruleset):
    ruleset_name = os.path.basename(path_to_ruleset)

    compiled_ruleset = os.path.join(rulebank_base_directory, '{ruleset}.dpgr'.format(ruleset=ruleset_name))

    with zipfile.PyZipFile(compiled_ruleset, mode='w') as ruleset:
        mock_ruleset_directory = os.path.join(os.path.dirname(__file__), ruleset_name)
        ruleset.writepy(pathname=mock_ruleset_directory)


@pytest.yield_fixture(params=('mock_ruleset_simple', 'mock_ruleset_multifile'))
def installed_ruleset(tempdir: tempfile.TemporaryDirectory, request):
    compile_folder_and_install_as_ruleset(tempdir.name, request.param)
    yield request.param


def test_loads_rule_bank_from_rulebank_path(tempdir, installed_ruleset):
    loaded = rule_bank.load_rule_bank(directory=tempdir.name)

    strategy = loaded.get_strategy(installed_ruleset)
    assert type(strategy) == rule_bank.RuleSet
    result = strategy.generate_password(['a', 'b', 'c'])
    assert result == 'abc'


if __name__ == '__main__':
    import pytest

    pytest.main(__file__)
