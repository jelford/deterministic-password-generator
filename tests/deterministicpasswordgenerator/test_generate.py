from mock import MagicMock

from deterministicpasswordgenerator.generate import PasswordGenerator


def test_gets_ruleset_from_rule_bank_and_calls_with_parts():
    mock_rule_bank = MagicMock()
    mock_strategy = MagicMock()

    mock_rule_bank.get_strategy.return_value = mock_strategy
    mock_rule_bank.get_strategy.return_value = mock_strategy
    mock_strategy.generate.return_value = 'abc'

    under_test = PasswordGenerator(mock_rule_bank)
    result = under_test.generate('concatenate', ['a', 'b', 'c'])
    assert result == 'abc'

    mock_rule_bank.get_strategy.assert_called_once_with('concatenate')
    mock_strategy.generate.assert_called_once_with(['a', 'b', 'c'])
