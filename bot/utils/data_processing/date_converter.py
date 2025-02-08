import re
from datetime import date, datetime

RUS_MONTHS = {
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

MONTHS = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}


def parse_date(date_str: str) -> date:
    """
    Преобразует строку с датой в объект date.
    Поддерживает форматы: "дд.мм.гггг" и "ддмммгггг" 
    например, 2мар2025 -> 2025-03-02, 02.03.2025 -> 2025-03-02.
    """
    try:
        if re.fullmatch(r"\d{1,2}\.\d{2}\.\d{4}", date_str): 
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        
        elif re.fullmatch(r"\d{1,2}[а-я]{3}\d{4}", date_str):
            day = re.match(r"\d{1,2}", date_str).group()
            month = re.search(r"[а-я]{3}", date_str).group()
            year = re.search(r"\d{4}", date_str).group()

            if month in RUS_MONTHS:
                date_str = f"{day} {RUS_MONTHS[month]} {year}"
                return datetime.strptime(date_str, "%d %b %Y").date()
            
        return None
    except:
        return None

def format_date(date_input):
    """
    Преобразует date объект 2025-02-02 в "2 февраля 2025"
    """
    return f"{date_input.day} {MONTHS[date_input.month]} {date_input.year}"