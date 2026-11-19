"""Property-based tests for the bookstore trade-in input helpers."""

"""
Older code


from hypothesis import given, strategies as st
from processor import verify_isbn10_format, calculate_depreciation_factor, lookup_condition_multiplier

@given(st.text() | st.none())
def test_verify_isbn10_format_no_crash(s):
    # To-Do:Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_calculate_depreciation_factor_safe(s):
    # To-Do:Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_lookup_condition_multiplier_safe(s):
    # To-Do:Using try and except complete this function.
    pass
"""



import pytest
from hypothesis import given, strategies as st

from processor import (
    calculate_depreciation_factor,
    lookup_condition_multiplier,
    verify_isbn10_format,
)


@given(st.text() | st.none())
def test_verify_isbn10_format_no_crash(value):
    # Invalid user input may be rejected, but it must not cause an unexpected
    # exception such as IndexError or AttributeError.
    try:
        result = verify_isbn10_format(value)
    except (TypeError, ValueError):
        return

    assert result.startswith("Group ")
    assert ": Starts " in result
    assert ", Checksum " in result


@given(st.text() | st.none())
def test_calculate_depreciation_factor_safe(value):
    try:
        result = calculate_depreciation_factor(value)
    except (TypeError, ValueError):
        return

    assert isinstance(result, float)
    assert 0.1 <= result <= 1.0


@given(st.text() | st.none())
def test_lookup_condition_multiplier_safe(value):
    try:
        result = lookup_condition_multiplier(value)
    except (TypeError, ValueError):
        return

    assert result in {0.30, 0.60, 0.80, 1.00, 1.25}


def test_valid_examples():
    assert verify_isbn10_format("0-306-40615-2") == (
        "Group 306: Starts 0, Checksum 2"
    )
    assert verify_isbn10_format(" 030640615x ") == (
        "Group 306: Starts 0, Checksum X"
    )
    assert calculate_depreciation_factor("3/10") == 0.7
    assert calculate_depreciation_factor("10/10") == 0.1
    assert lookup_condition_multiplier(" mint ") == 1.25


@pytest.mark.parametrize(
    ("function", "value"),
    [
        (verify_isbn10_format, None),
        (verify_isbn10_format, ""),
        (verify_isbn10_format, "123456789? "),
        (calculate_depreciation_factor, None),
        (calculate_depreciation_factor, "1/0"),
        (calculate_depreciation_factor, "-1/10"),
        (calculate_depreciation_factor, "nan/10"),
        (lookup_condition_multiplier, None),
        (lookup_condition_multiplier, "excellent"),
    ],
)
def test_invalid_inputs_are_rejected_cleanly(function, value):
    with pytest.raises((TypeError, ValueError)):
        function(value)
