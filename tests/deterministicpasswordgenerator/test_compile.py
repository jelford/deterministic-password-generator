import zipfile

import pytest
import tempfile
from os import path

from deterministicpasswordgenerator.compile import compile_ruleset


@pytest.yield_fixture(params=['mock_ruleset_multifile', 'mock_ruleset_simple'])
def ruleset_name(request):
    yield request.param


def test_compiled_ruleset_can_be_read_by_parser(ruleset_name: str, tempdir: tempfile.TemporaryDirectory):
    from deterministicpasswordgenerator.rule_bank import load_rule_bank
    path_to_ruleset = path.join(path.dirname(path.abspath(__file__)), ruleset_name)
    assert path.isdir(path_to_ruleset)
    compile_ruleset(path_to_ruleset, output_path=tempdir.name)
    rule_bank = load_rule_bank(directory=tempdir.name)
    assert rule_bank.get_strategy(ruleset_name) is not None


def test_compiled_ruleset_is_not_readable(ruleset_name, tempdir: tempfile.TemporaryDirectory):
    path_to_ruleset = path.join(path.dirname(path.abspath(__file__)), ruleset_name)
    compile_ruleset(path_to_ruleset, output_path=tempdir.name)
    with pytest.raises(zipfile.BadZipfile):
        zipfile.ZipFile(path.join(tempdir.name, ruleset_name + '.dpgr'))
