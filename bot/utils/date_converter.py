from datetime import date, datetime
import re


def convert_to_short_format(date_str: str) -> str:
    """
    Преобразует дату в короткий формат (например, "1 января 2024" -> "1янв2024").
    Поддерживает даты, разделённые дефисом.
    """
    parts = date_str.split("-")
    formatted_dates = []
    short_month_dict = {
        "января": "янв", "февраля": "фев", "марта": "мар", "апреля": "апр",
        "мая": "май", "июня": "июн", "июля": "июл", "августа": "авг",
        "сентября": "сен", "октября": "окт", "ноября": "ноя", "декабря": "дек"
    }
    
    for part in parts:
        match = re.match(r"(\d{1,2}) (\D+) (\d{4})", part)  # Проверяем формат "1 января 2024"
        if match:
            day, month, year = match.groups()
            if month in short_month_dict:
                formatted_dates.append(f"{int(day)}{short_month_dict[month]}{year}")
                continue

        match = re.match(r"(\d{1,2})([а-я]{3})(\d{4})", part)  # Проверяем короткий формат
        if match:
            formatted_dates.append(part)
            continue

        return None

    return "-".join(formatted_dates)


def parse_date(date_str: str) -> date:
    """
    Преобразует строку с датой в объект date.
    Поддерживает форматы: "дд.мм.гггг" и "ддмммгггг" (например, "1.01.2024" или "1янв2024").
    """
    rus_month_dict = {
        "янв": "Jan", "фев": "Feb", "мар": "Mar", "апр": "Apr",
        "мая": "May", "май": "May", "июн": "Jun", "июл": "Jul", "авг": "Aug",
        "сен": "Sep", "окт": "Oct", "ноя": "Nov", "дек": "Dec"
    }
    try:
        if re.fullmatch(r"\d{1,2}\.\d{2}\.\d{4}", date_str):  # Проверяем формат "дд.мм.гггг"
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        elif re.fullmatch(r"\d{1,2}[а-я]{3}\d{4}", date_str):  # Проверяем формат "ддмммгггг"
            day = re.match(r"\d{1,2}", date_str).group()  
            month = re.search(r"[а-я]{3}", date_str).group() 
            year = re.search(r"\d{4}", date_str).group() 
            if month in rus_month_dict:
                date_str = f"{day} {rus_month_dict[month]} {year}"
                return datetime.strptime(date_str, "%d %b %Y").date()
        return None  
    except (ValueError, AttributeError):
        return None


def convert_date_part(date_part: str) -> str:
    """
    Преобразует короткий формат даты в полный (например, "1янв2024" -> "1 января 2024").
    """
    full_month_dict = {
        "янв": "января", "фев": "февраля", "мар": "марта", "апр": "апреля",
        "май": "мая", "мая": "мая", "июн": "июня", "июл": "июля", "авг": "августа",
        "сен": "сентября", "окт": "октября", "ноя": "ноября", "дек": "декабря"
    }

    if "." in date_part:  # Проверяем формат "дд.мм.гггг"
        day, month, year = date_part.split(".")
        month = int(month)
    else:  # Проверяем короткий формат "ддмммгггг"
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
    """
    Преобразует строку с датой в формат, удобный для хранения в базе данных.
    Например, "1янв2024-2фев2025" -> "1 января 2024 - 2 февраля 2025".
    """
    parts = date.split("-")
    return "-".join(convert_date_part(part) for part in parts)
