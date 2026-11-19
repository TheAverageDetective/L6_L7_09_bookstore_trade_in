"""Bookstore trade-in helpers exercised by the Lab 7 fuzz tests."""

import math


def verify_isbn10_format(isbn_str):
    """Validate ISBN-10 characters and return its displayed components.

    Hyphens may be used as visual separators and surrounding whitespace is
    ignored. This checks the ISBN-10 format; it does not verify the checksum.
    """
    if not isinstance(isbn_str, str):
        raise TypeError("ISBN must be a string")

    cleaned = isbn_str.replace("-", "").strip()
    if len(cleaned) != 10:
        raise ValueError("ISBN-10 must contain exactly 10 characters")
    if any(character not in "0123456789" for character in cleaned[:9]):
        raise ValueError("The first nine ISBN-10 characters must be digits")

    check_char = cleaned[9].upper()
    if not (check_char in "0123456789" or check_char == "X"):
        raise ValueError("The ISBN-10 check character must be a digit or X")

    first_digit = int(cleaned[0])
    group_code = cleaned[1:4]
    return f"Group {group_code}: Starts {first_digit}, Checksum {check_char}"


def calculate_depreciation_factor(book_age_str):
    """Return the trade-in depreciation factor for ``age/lifespan`` years."""
    if not isinstance(book_age_str, str):
        raise TypeError("Age and lifespan must be provided as a string")

    parts = book_age_str.split("/")
    if len(parts) != 2:
        raise ValueError("Age and lifespan must have the form age/lifespan")

    try:
        age, life = (float(part.strip()) for part in parts)
    except ValueError as exc:
        raise ValueError("Age and lifespan must be numeric") from exc

    if not math.isfinite(age) or not math.isfinite(life):
        raise ValueError("Age and lifespan must be finite numbers")
    if age < 0:
        raise ValueError("Age cannot be negative")
    if life <= 0:
        raise ValueError("Lifespan must be greater than zero")

    depreciation = 1.0 - (age / life)
    return round(max(0.1, depreciation), 2)


def lookup_condition_multiplier(condition_code):
    """Return the trade-in multiplier for a supported book condition."""
    if not isinstance(condition_code, str):
        raise TypeError("Condition must be a string")

    grade = condition_code.strip().upper()
    multipliers = {
        "MINT": 1.25,
        "LIKE_NEW": 1.00,
        "VERY_GOOD": 0.80,
        "GOOD": 0.60,
        "POOR": 0.30,
    }
    try:
        return multipliers[grade]
    except KeyError as exc:
        raise ValueError(f"Unknown book condition: {condition_code!r}") from exc


def main():
    print("==== Running verify_isbn10_format ====")
    isbn_in = input("Enter ISBN-10 (e.g. 0-306-40615-2): ")
    print(verify_isbn10_format(isbn_in))

    print("\n==== Running calculate_depreciation_factor ====")
    age_in = input("Enter age/lifespan in years (e.g. 3/10): ")
    print("Depreciation Factor:", calculate_depreciation_factor(age_in))

    print("\n==== Running lookup_condition_multiplier ====")
    cond_in = input("Enter condition (e.g. MINT, GOOD, POOR): ")
    print("Multiplier:", lookup_condition_multiplier(cond_in))


if __name__ == "__main__":
    main()
