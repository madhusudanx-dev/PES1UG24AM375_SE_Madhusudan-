from hypothesis import given, strategies as st
from pet_boarding import parse_booking, stay_average, payable_fee

# ---------------------------------------------------------------------------
# Lab 7 - Fuzz Testing
# Group: L6_L7_49 | SRN: PES1UG24AM375 | Name: Madhusudan P
#
# Each function is fuzzed with random text (and None). The invariant is:
#   "malformed input is rejected cleanly with ValueError, and valid input
#    returns a well-formed result."
# Any OTHER exception (AttributeError, TypeError, ZeroDivisionError, ...)
# escapes the try/except and FAILS the test - that is how fuzzing catches
# uncontrolled crashes.
# ---------------------------------------------------------------------------


@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        pet, days = parse_booking(s)
    except ValueError:
        return  # malformed input rejected cleanly - acceptable
    # valid input -> result must be well-formed
    assert isinstance(pet, str)
    assert isinstance(days, float)


@given(st.text() | st.none())
def test_stay_average_no_crash(s):
    try:
        result = stay_average(s)
    except ValueError:
        return
    assert isinstance(result, int)


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        result = payable_fee(s)
    except ValueError:
        return
    assert result >= 0  # fee is never negative


# ---------------------------------------------------------------------------
# Additional property-based tests that steer Hypothesis toward the VALID
# paths (random free text almost never forms a legal 'pet:days' string),
# so the happy-path invariants are actually exercised, not just the
# rejection path.
# ---------------------------------------------------------------------------

# text without the delimiters, so we can build well-formed inputs
_pet_name = st.text(
    alphabet=st.characters(blacklist_characters=":|,"), min_size=1
).filter(lambda p: p.strip() != "")
_finite = st.floats(allow_nan=False, allow_infinity=False,
                    min_value=-1e9, max_value=1e9)


@given(_pet_name, _finite)
def test_parse_booking_roundtrip(pet, days):
    result_pet, result_days = parse_booking(f"{pet}:{days}")
    assert result_pet == pet.strip().title()
    assert result_days == days


@given(st.lists(st.integers(min_value=-1000, max_value=1000), min_size=1))
def test_stay_average_within_bounds(nums):
    csv = ",".join(str(n) for n in nums)
    result = stay_average(csv)
    # an integer average always lies between the min and max of the inputs
    assert min(nums) <= result <= max(nums)
    assert isinstance(result, int)


@given(_finite, _finite)
def test_payable_fee_never_negative(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    assert result >= 0


@given(st.sampled_from([None, 123, 4.5, [], {}, ("a",)]))
def test_non_string_inputs_rejected(bad):
    # every non-string argument must raise ValueError, never a raw TypeError
    for fn in (parse_booking, stay_average, payable_fee):
        try:
            fn(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{fn.__name__} accepted non-string {bad!r}")
