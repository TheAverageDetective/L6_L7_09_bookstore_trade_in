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