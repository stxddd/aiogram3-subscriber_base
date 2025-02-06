import re
from datetime import date, datetime

from bot.utils.data_processing.date_converter import parse_date


def is_correct_date_part(date_str: str):
    """
    Вернет false если дата не соответсует шаблону, иначе True
    """
    pattern = r"(\d{1,2}[а-я]{3}\d{4}|\d{2}\.\d{2}\.\d{4})(-\d{1,2}[а-я]{3}\d{4})?"
    
    return re.fullmatch(pattern, date_str)


def is_valid_date(date_str: str):
    """
    Вернет False, если даты не по одному из шаблонов или некорректны:
    1) 1фев2025-2фев2025 
    2) 01.02.2025-02.02.2005 
    3) 2025-02-01.2025-02-01
    Иначе массив [start_date, end_date] типа date.
    """

    base_pattern = re.fullmatch(r"(\d{1,2}\.\d{2}\.\d{4}|\d{1,2}[а-я]{3}\d{4})-(\d{1,2}\.\d{2}\.\d{4}|\d{1,2}[а-я]{3}\d{4})", date_str)
    date_format_pattern = re.fullmatch(r"\d{4}-\d{2}-\d{2}\.\d{4}-\d{2}-\d{2}", date_str)

    if not base_pattern and not date_format_pattern:
        return False

    if base_pattern:
        start_date_str, end_date_str = date_str.split("-")
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
    else:  
        start_date_str, end_date_str = date_str.split(".")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    today = date.today()
    if not start_date or not end_date:
        return False
    if start_date > end_date:
        return False
    if end_date < today:
        return False

    return [start_date, end_date]

def is_valid_price(price: str) -> bool:
    return price.isdigit()


def is_valid_name(name: str) -> bool:
    return len(name) <= 32
