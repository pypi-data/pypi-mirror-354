import pytest
from owlsight.ui.console import Selector
from owlsight.ui.custom_classes import OptionType


@pytest.fixture
def options_dict():
    """
    Fixture that provides a standard dictionary with editable input,
    static options, and a toggle option.
    """
    return {
        "You are a:": "",  # Editable input
        "apple": None,  # Static option
        "pear": None,  # Static option
        "Is it ripe?": [True, False],  # Toggleable option
    }


def test_selector_initialization(options_dict):
    """
    Test that the Selector class correctly initializes with options.
    """
    selector = Selector(options_dict)

    # Ensure that the options are properly parsed and initialized
    assert len(selector.options) == 4
    assert selector.options[0] == ("You are a:", OptionType.EDITABLE)
    assert selector.options[1] == ("apple", OptionType.ACTION)
    assert selector.options[2] == ("pear", OptionType.ACTION)
    assert selector.options[3] == ("Is it ripe?", OptionType.TOGGLE)

    # Ensure that the initial values of user inputs and toggles are correct
    assert selector.user_inputs == {"You are a:": ""}
    assert selector.toggle_values == {"Is it ripe?": True}
    assert selector.current_index == 0
