import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status

# ---------------------------------------------------------------------------
# Lab 6 - Code and Branch Coverage
# Group: L6_L7_49 | SRN: PES1UG24AM375 | Name: Madhusudan P
#
# The tests below exercise every statement AND every branch of
# pet_boarding.py (100% statement + 100% branch coverage).
# ---------------------------------------------------------------------------


# ===========================================================================
# boarding_fee(pet_type, days, is_premium)
# ===========================================================================

def test_within_included_days():
    # extra <= 0 branch (days inside the free allowance) -> 0
    assert boarding_fee("dog", 1, False) == 0


def test_unknown_pet_type_raises():
    # pet_type not in INCLUDED_DAYS branch
    with pytest.raises(ValueError):
        boarding_fee("hamster", 5, False)


def test_negative_days_raises():
    # days < 0 branch
    with pytest.raises(ValueError):
        boarding_fee("cat", -1, False)


def test_premium_adds_a_day_for_dog():
    # is_premium and pet_type != "rabbit" branch (True)
    # dog included = 2, premium -> 3, so 3 days still free
    assert boarding_fee("dog", 3, True) == 0


def test_premium_ignored_for_rabbit():
    # is_premium True but pet_type == "rabbit" -> the AND is False
    # rabbit included = 4, premium makes no difference; 5 days -> 1 extra day
    assert boarding_fee("rabbit", 5, True) == 20


def test_dog_extra_days_rate_30():
    # pet_type == "dog" branch, extra <= 10 (no surcharge)
    # included 2, days 5 -> extra 3 * 30 = 90
    assert boarding_fee("dog", 5, False) == 90


def test_cat_extra_days_rate_20():
    # else branch (non-dog rate = 20), extra <= 10
    # included 3, days 6 -> extra 3 * 20 = 60
    assert boarding_fee("cat", 6, False) == 60


def test_dog_long_stay_surcharge():
    # extra > 10 branch AND nested pet_type == "dog" branch
    # included 2, days 15 -> extra 13; rate 30 + 10 + 5 = 45; 13 * 45 = 585
    assert boarding_fee("dog", 15, False) == 585


def test_cat_long_stay_surcharge_no_dog_bonus():
    # extra > 10 branch, nested pet_type == "dog" is False
    # included 3, days 15 -> extra 12; rate 20 + 10 = 30; 12 * 30 = 360
    assert boarding_fee("cat", 15, False) == 360


def test_rabbit_extra_days_rate_20():
    # rabbit uses else rate (20), extra <= 10
    # included 4, days 6 -> extra 2 * 20 = 40
    assert boarding_fee("rabbit", 6, False) == 40


def test_extra_exactly_zero_boundary():
    # boundary: extra == 0 falls into the extra <= 0 branch
    # cat included 3, days 3 -> extra 0 -> 0
    assert boarding_fee("cat", 3, False) == 0


# ===========================================================================
# admission_ok(pet_age_years, vaccinations, is_senior)
# ===========================================================================

def test_admission_ok():
    # non-senior, age >= 1, vaccinations >= 2 -> True
    assert admission_ok(4, 2, False) is True


def test_admission_senior_enough_vaccinations():
    # is_senior branch (True), vaccinations >= 3 -> True
    assert admission_ok(9, 3, True) is True


def test_admission_senior_too_few_vaccinations():
    # is_senior branch (True), vaccinations < 3 -> False
    assert admission_ok(9, 2, True) is False


def test_admission_young_pet_rejected():
    # non-senior, pet_age_years < 1 branch -> False
    assert admission_ok(0, 5, False) is False


def test_admission_adult_too_few_vaccinations():
    # non-senior, age >= 1, vaccinations < 2 -> False
    assert admission_ok(3, 1, False) is False


# ===========================================================================
# checkout_status(minutes_left, is_long_stay, is_weekend)
# ===========================================================================

def test_checkout_open_short_weekday():
    # is_long_stay False -> cutoff 15; not weekend; minutes >= cutoff -> open
    assert checkout_status(20, False, False) == "open"


def test_checkout_late_short_weekday():
    # cutoff 15; minutes in [cutoff-15, cutoff) -> late
    assert checkout_status(5, False, False) == "late"


def test_checkout_closed_short_weekday():
    # cutoff 15; minutes < cutoff - 15 -> closed
    assert checkout_status(-1, False, False) == "closed"


def test_checkout_long_stay_cutoff():
    # is_long_stay True -> cutoff 30; 29 < 30 but >= 15 -> late
    assert checkout_status(29, True, False) == "late"


def test_checkout_weekend_raises_cutoff():
    # is_weekend True -> cutoff += 20; short stay cutoff 15 + 20 = 35
    # 34 is < 35 but >= 20 -> late (confirms the weekend branch ran)
    assert checkout_status(34, False, True) == "late"


def test_checkout_long_stay_weekend_open():
    # both branches: cutoff 30 + 20 = 50; 50 >= 50 -> open
    assert checkout_status(50, True, True) == "open"


def test_checkout_boundary_open_exact():
    # minutes_left exactly == cutoff -> open (boundary)
    assert checkout_status(15, False, False) == "open"
