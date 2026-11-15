"""Lab 7 - Fuzz Testing (hardened module).

Group: L6_L7_49 | SRN: PES1UG24AM375 | Name: Madhusudan P

Fuzz testing with Hypothesis on the original code revealed several
uncontrolled crashes on malformed input, e.g.:

  * parse_booking(None)      -> AttributeError  ('NoneType' has no 'split')
  * parse_booking("")        -> ValueError      (not enough values to unpack)
  * parse_booking("a:b:c")   -> ValueError      (too many values to unpack)
  * parse_booking("dog:x")   -> ValueError      (could not convert 'x' to float)
  * stay_average(None)       -> AttributeError
  * stay_average("")         -> ValueError      (int('') )
  * stay_average("1,x")      -> ValueError      (int('x') )
  * payable_fee(None)        -> AttributeError
  * payable_fee("")          -> ValueError      (unpack)
  * payable_fee("x|1")       -> ValueError      (float('x') )

The functions below are hardened so that ALL malformed input is rejected
with a single, documented exception type (ValueError). No other exception
type can escape, which is exactly the invariant the fuzz tests check.
Happy-path behaviour is unchanged from the original.
"""


def parse_booking(text):
    """Parse 'pet:days' into (TitleCasePet, days_as_float).

    Raises ValueError for any malformed input.
    """
    if not isinstance(text, str):
        raise ValueError("booking must be a string")
    parts = text.split(':')
    if len(parts) != 2:
        raise ValueError("booking must be in 'pet:days' format")
    pet, days = parts
    pet = pet.strip().title()
    if not pet:
        raise ValueError("pet name must not be empty")
    try:
        days_value = float(days)
    except ValueError:
        raise ValueError("days must be a number")
    return pet, days_value


def stay_average(days_csv):
    """Integer-average of a comma-separated list of stay lengths.

    Raises ValueError for any malformed input.
    """
    if not isinstance(days_csv, str):
        raise ValueError("stay lengths must be a string")
    parts = [r.strip() for r in days_csv.split(',')]
    try:
        values = [int(r) for r in parts]
    except ValueError:
        raise ValueError("every stay length must be an integer")
    if not values:
        raise ValueError("no stay lengths provided")
    return sum(values) // len(values)


def payable_fee(text):
    """Compute payable fee from 'fee|discount' (18% tax, never below 0).

    Raises ValueError for any malformed input.
    """
    if not isinstance(text, str):
        raise ValueError("input must be a string")
    parts = text.split('|')
    if len(parts) != 2:
        raise ValueError("input must be in 'fee|discount' format")
    fee_text, discount_text = parts
    try:
        fee = float(fee_text)
        discount = float(discount_text)
    except ValueError:
        raise ValueError("fee and discount must be numbers")
    total = fee * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_booking ====")
    try:
        user_input = input("Enter pet:days (e.g. dog:5): ")
        print("Pet and Days:", parse_booking(user_input))
    except ValueError as exc:
        print("Invalid input:", exc)

    print("\n==== Running stay_average ====")
    try:
        user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
        print("Average Stay:", stay_average(user_input))
    except ValueError as exc:
        print("Invalid input:", exc)

    print("\n==== Running payable_fee ====")
    try:
        user_input = input("Enter fee|discount (e.g. 1500|100): ")
        print("Payable Fee:", payable_fee(user_input))
    except ValueError as exc:
        print("Invalid input:", exc)


if __name__ == "__main__":
    main()
