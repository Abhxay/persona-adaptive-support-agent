import pytest
from persona_detector import detect_persona  # assuming the detection function is named accordingly


def test_valid_persona_detection():
    assert detect_persona("user input example") == "expected persona"


def test_invalid_input():
    with pytest.raises(ValueError):
        detect_persona(None)


@pytest.mark.parametrize("input, expected", [
    ("example input 1", "expected persona 1"),
    ("example input 2", "expected persona 2"),
])
def test_persona_detection_parametrized(input, expected):
    assert detect_persona(input) == expected
