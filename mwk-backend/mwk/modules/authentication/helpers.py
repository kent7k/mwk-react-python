from datetime import date, timedelta


def is_age_at_least(birthday: date, age: int) -> bool:
    """
    Accepts the birthday date and checks that the person is at least `age` years old.

    Args:
        birthday: The birthday date of the person to be checked.
        age: The age limit to be checked against.

    Returns:
        True if the person is at least `age` years old, False otherwise.
    """
    age_reached = birthday + timedelta(days=age*365)
    return date.today() >= age_reached


def contains_digits(string: str) -> bool:
    """
    Returns True if the given string contains any digits.

    Args:
        string: The string to be checked for digits.

    Returns:
        True if the string contains digits, False otherwise.
    """
    return any(char.isdigit() for char in string)
