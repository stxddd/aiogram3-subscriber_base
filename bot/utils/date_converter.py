from datetime import date, datetime
import re




def parse_date(date_str: str) -> date:
    month_dict = {
        "янв": "Jan", "фев": "Feb", "мар": "Mar", "апр": "Apr",
        "май": "May", "июн": "Jun", "июл": "Jul", "авг": "Aug",
        "сен": "Sep", "окт": "Oct", "ноя": "Nov", "дек": "Dec"
    }
    try:
        if re.fullmatch(r"\d{1,2}\.\d{2}\.\d{4}", date_str):  # Формат дд.мм.гггг
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        elif re.fullmatch(r"\d{1,2}[а-я]{3}\d{4}", date_str):  # Формат dMMMYYYY (1фев2025)
            day = re.match(r"\d{1,2}", date_str).group()  
            month = re.search(r"[а-я]{3}", date_str).group() 
            year = re.search(r"\d{4}", date_str).group() 
            if month in month_dict:
                date = f"{day} {month_dict[month]} {year}"
                return datetime.strptime(date, "%d %b %Y").date()
        return None  
    except (ValueError, AttributeError):
        return None

MONTHS = {
    "янв": "января", "фев": "февраля", "мар": "марта", "апр": "апреля",
    "май": "мая", "июн": "июня", "июл": "июля", "авг": "августа",
    "сен": "сентября", "окт": "октября", "ноя": "ноября", "дек": "декабря"
}

def convert_date_part(date_part: str) -> str:
    if "." in date_part: 
        day, month, year = date_part.split(".")
        month = int(month)
    else:  
        for key in MONTHS.keys():
            if key in date_part:
                day, rest = date_part.split(key)
                month = key
                year = rest
                break
        else:
            return date_part 

        return f"{int(day)} {MONTHS[month]} {year}"

    return f"{int(day)} {MONTHS[list(MONTHS.keys())[month - 1]]} {year}"

def get_date_for_db(date: str) -> str:
    parts = date.split("-")
    return "-".join(convert_date_part(part) for part in parts)
