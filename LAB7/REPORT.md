# Lab 7 Report: Fuzz Testing for Pet Boarding

**Group:** L6_L7_49  
**SRN:** PES1UG24AM375  
**Name:** Madhusudan P

## Aim

Harden pet boarding input-processing functions and describe property-based fuzz tests that check how they handle malformed and valid inputs.

## Implementation

`pet_boarding.py` provides three functions:

- `parse_booking(text)` parses a `pet:days` booking and returns a title-cased pet name with the stay length as a float.
- `stay_average(days_csv)` parses comma-separated integer stay lengths and returns their integer average.
- `payable_fee(text)` parses `fee|discount`, applies 18% tax, subtracts the discount, and floors the payable amount at zero.

The functions validate input types and formats and report malformed input using `ValueError`. The module also includes an interactive `main()` entry point.

## Test approach

`test_pet_boarding.py` uses Hypothesis strategies to generate arbitrary text and `None` for malformed-input checks, and targeted valid inputs for property checks. The properties cover result types and shapes, average bounds, nonnegative payable fees, and rejection of non-string values.

## Running the tests

Install Hypothesis and pytest if needed, then run from this folder:

```bash
python -m pytest -q test_pet_boarding.py
```

This report describes the supplied test suite; the tests were not executed while preparing these files.
