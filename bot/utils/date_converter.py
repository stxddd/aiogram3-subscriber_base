from datetime import date, datetime
import re


def convert_to_short_format(date_str: str) -> str:
    parts = date_str.split("-")
    formatted_dates = []
    short_month_dict = {
    "января": "янв", "февраля": "фев", "марта": "мар", "апреля": "апр",
    "мая": "май", "июня": "июн", "июля": "июл", "августа": "авг",
    "сентября": "сен", "октября": "окт", "ноября": "ноя", "декабря": "дек"
    }
    for part in parts:
        match = re.match(r"(\d{1,2}) (\D+) (\d{4})", part) 
        if match:
            day, month, year = match.groups()
            if month in short_month_dict:
                formatted_dates.append(f"{int(day)}{short_month_dict[month]}{year}")
                continue

        match = re.match(r"(\d{1,2})([а-я]{3})(\d{4})", part) 
        if match:
            formatted_dates.append(part)
            continue

        return None

    return "-".join(formatted_dates)


def parse_date(date_str: str) -> date:
    rus_month_dict = {
        "янв": "Jan", "фев": "Feb", "мар": "Mar", "апр": "Apr",
        "мая": "May","май": "May", "июн": "Jun", "июл": "Jul", "авг": "Aug",
        "сен": "Sep", "окт": "Oct", "ноя": "Nov", "дек": "Dec"
    }
    try:
        if re.fullmatch(r"\d{1,2}\.\d{2}\.\d{4}", date_str): 
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        elif re.fullmatch(r"\d{1,2}[а-я]{3}\d{4}", date_str): 
            day = re.match(r"\d{1,2}", date_str).group()  
            month = re.search(r"[а-я]{3}", date_str).group() 
            year = re.search(r"\d{4}", date_str).group() 
            if month in rus_month_dict:
                date = f"{day} {rus_month_dict[month]} {year}"
                return datetime.strptime(date, "%d %b %Y").date()
        return None  
    except (ValueError, AttributeError):
        return None


def convert_date_part(date_part: str) -> str:
    full_month_dict = {
    "янв": "января", "фев": "февраля", "мар": "марта", "апр": "апреля",
    "май": "мая", "мая": "мая", "июн": "июня", "июл": "июля", "авг": "августа",
    "сен": "сентября", "окт": "октября", "ноя": "ноября", "дек": "декабря"
    }

    if "." in date_part: 
        day, month, year = date_part.split(".")
        month = int(month)
    else:  
        for key in full_month_dict.keys():
            if key in date_part:
                day, rest = date_part.split(key)
                month = key
                year = rest
                break
        else:
            return date_part 

        return f"{int(day)} {full_month_dict[month]} {year}"

    return f"{int(day)} {full_month_dict[list(full_month_dict.keys())[month - 1]]} {year}"



def get_date_for_db(date: str) -> str:
    parts = date.split("-")
    return "-".join(convert_date_part(part) for part in parts)
