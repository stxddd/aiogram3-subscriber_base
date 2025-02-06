import re
from datetime import date, datetime


def parse_date(date_str: str) -> date:
    """
    Преобразует строку с датой в объект date.
    Поддерживает форматы: "дд.мм.гггг" и "ддмммгггг" 
    например, 2мар2025 -> 2025-03-02, 02.03.2025 -> 2025-03-02.
    """
    rus_month_dict = {
        "янв": "Jan",
        "фев": "Feb",
        "мар": "Mar",
        "апр": "Apr",
        "мая": "May",
        "май": "May",
        "июн": "Jun",
        "июл": "Jul",
        "авг": "Aug",
        "сен": "Sep",
        "окт": "Oct",
        "ноя": "Nov",
        "дек": "Dec",
    }
    try:
        if re.fullmatch(r"\d{1,2}\.\d{2}\.\d{4}", date_str): 
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        
        elif re.fullmatch(r"\d{1,2}[а-я]{3}\d{4}", date_str):
            day = re.match(r"\d{1,2}", date_str).group()
            month = re.search(r"[а-я]{3}", date_str).group()
            year = re.search(r"\d{4}", date_str).group()

            if month in rus_month_dict:
                date_str = f"{day} {rus_month_dict[month]} {year}"
                return datetime.strptime(date_str, "%d %b %Y").date()
            
        return None
    except (ValueError, AttributeError):
        return None

def format_date(date_input):
    """
    Преобразует date объект 2025-02-02 в "2 февраля 2025"
    """
    months = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля",
        5: "мая", 6: "июня", 7: "июля", 8: "августа",
        9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }

    return f"{date_input.day} {months[date_input.month]} {date_input.year}"