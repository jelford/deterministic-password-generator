import pytest
from mock import MagicMock

from deterministicpasswordgenerator.generate import PasswordGenerator, generate_password
from deterministicpasswordgenerator.rule_bank import RuleBank, RuleSet


def test_gets_ruleset_from_rule_bank_and_calls_with_parts():
    mock_rule_bank = MagicMock(spec=RuleBank)
    mock_strategy = MagicMock(spec=RuleSet)

    mock_rule_bank.get_strategy.return_value = mock_strategy
    mock_strategy.generate_password.return_value = 'abc'

    under_test = PasswordGenerator(mock_rule_bank)
    result = under_test.generate('concatenate', ['a', 'b', 'c'])
    assert result == 'abc'

    mock_rule_bank.get_strategy.assert_called_once_with('concatenate')
    mock_strategy.generate_password.assert_called_once_with(['a', 'b', 'c'])


def test_requests_decryption_key_if_none_given(mocker):
    mocker.patch('deterministicpasswordgenerator.generate.getpass',
                 side_effect=RequestedPasswordInput())

    mocker.patch('builtins.input',
                 side_effect=Forbidden('Shouldn\'t ask for plain-text input of password'))
    mocker.patch('deterministicpasswordgenerator.generate.load_rule_bank',
                 side_effect=Forbidden('Shouldn\'t get this far'))

    with pytest.raises(RequestedPasswordInput):
        generate_password('ruleset_name', ('p', 'a', 'r', 't', 's'))


class RequestedPasswordInput(RuntimeError):
    pass


class Forbidden(AssertionError):
    pass
