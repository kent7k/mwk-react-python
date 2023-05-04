from datetime import date, timedelta


def is_age_at_least(birthday: date, age: int) -> bool:
    age_reached = birthday + timedelta(days=age*365)
    return date.today() >= age_reached


def contains_digits(string: str) -> bool:
    return any(char.isdigit() for char in string)
