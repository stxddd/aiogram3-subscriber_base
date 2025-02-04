import re
from datetime import date

from bot.utils.data_processing.date_converter import parse_date


def is_valid_date_part(date_str: str) -> bool:
    return bool(re.fullmatch(r"\d{1,2}[а-я]{3}\d{4}(-\d{1,2}[а-я]{3}\d{4})?", date_str))


def is_valid_date(date_str: str) -> bool:
    pattern = r"(\d{1,2}\.\d{2}\.\d{4}|\d{1,2}[а-я]{3}\d{4})-(\d{1,2}\.\d{2}\.\d{4}|\d{1,2}[а-я]{3}\d{4})"

    if not re.fullmatch(pattern, date_str):
        return False

    start_date_str, end_date_str = date_str.split("-")

    start_date = parse_date(start_date_str)
    end_date = parse_date(end_date_str)
    today = date.today()

    if not start_date or not end_date:
        return False
    if start_date > end_date:
        return False
    if end_date < today:
        return False

    return True


def is_valid_price(price: str) -> bool:
    return price.isdigit()


def is_valid_name(name: str) -> bool:
    return len(name) <= 32
