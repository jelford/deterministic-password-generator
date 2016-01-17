import zipfile

import pytest
import tempfile
from os import path

from deterministicpasswordgenerator.compile import compile_ruleset
from deterministicpasswordgenerator.rule_bank import load_rule_bank


@pytest.yield_fixture(params=['mock_ruleset_multifile', 'mock_ruleset_simple'])
def ruleset_name(request):
    yield request.param


def test_compiled_ruleset_can_be_read_by_parser(ruleset_name: str, tempdir: tempfile.TemporaryDirectory):
    path_to_ruleset = rulset_path(ruleset_name)
    assert path.isdir(path_to_ruleset)
    compile_ruleset(path_to_ruleset, output_path=tempdir.name, ruleset_encryption_password='encryption-key')
    rule_bank = load_rule_bank(directory=tempdir.name, encryption_key='encryption-key')
    assert rule_bank.get_strategy(ruleset_name) is not None


def test_compiled_ruleset_is_not_readable(ruleset_name, tempdir: tempfile.TemporaryDirectory):
    path_to_ruleset = rulset_path(ruleset_name)
    compile_ruleset(path_to_ruleset, output_path=tempdir.name, ruleset_encryption_password='encryption-key')
    with pytest.raises(zipfile.BadZipfile):
        zipfile.ZipFile(path.join(tempdir.name, ruleset_name + '.dpgr'))


def test_compile_asks_for_password_if_none_given(ruleset_name, mocker, tempdir: tempfile.TemporaryDirectory):
    mocker.patch('deterministicpasswordgenerator.compile.getpass', side_effect=RequestedPasswordInput())

    mocker.patch('builtins.input', side_effect=Forbidden('Should use password-input mode for password'))

    with pytest.raises(RequestedPasswordInput):
        compile_ruleset(rulset_path(ruleset_name), output_path=tempdir.name)


def rulset_path(ruleset_name: str):
    path_to_ruleset = path.join(path.dirname(path.abspath(__file__)), ruleset_name)
    return path_to_ruleset


class RequestedPasswordInput(RuntimeError):
    pass


class Forbidden(AssertionError):
    pass
