from aiogram.utils.markdown import hbold, hitalic

welcome_message = "Привет!🤖 \n\n✅ Данный Бот поможет вести базу абонентов, которым Вы предоставили доступ на ограниченное время к своим услугам.\n\n🔔Вы будете получать уведомления, когда клиенту будет необходимо пополнить баланс.\n\n💾 В любой момент Вы можете запросить свою базу в формате excel, изменить ее, удалить."
action_is_cancel_text = '❌ Действие отменено.'

enter_table_name_message = "❔Введите название таблицы (до 32 символов)."
pick_table_for_download_message = "❔Выберите таблицу, которую хотите скачать."
our_tables_message = "✅ Ваши таблицы"
table_are_missing_message = "❌ В настоящие время у Вас нет таблиц."
def are_you_sure_to_delete_table_message(table_name): return f'❔ Вы уверены, что хотите удалить таблицу «{table_name}»?'
def table_are_deleted_message(table_name): return f"✅ Таблица «{table_name}» удалена!"
def table_are_not_deleted_message(table_name): return f"❌ Невозможно удалить таблицу «{table_name}»!"
def select_an_action_for_the_table_message(table_name): return f'❔Выберите, что Вы хотите изменить в таблице «{table_name}»?'
def enter_new_table_name_message(table_name): return f'❔ Введите новое имя для таблицы «{table_name}» (до 32 символов)'
def table_name_message(table_name) -> str: return f"✅ Таблица: «{table_name}»"
def table_has_been_created_message(table_name): return f"💾✅ Создана таблица: «{table_name}»"
def table_has_no_lines_message(table_name): return f"✅ Записей в таблице «{table_name}» нет."
def table_name_changed_successfully_message(table_name, current_table_name): return f"✅ Таблица «{current_table_name}» переименована.\n\n{current_table_name} > {table_name}"
def table_has_no_lines_message(table_name): return f"❌ В таблице «{table_name}» нет данных!"

def one_line_message(line, table_name):
    text = (
    f"Выбрана строка таблицы «{hitalic(table_name)}»\n"
    f"{'➖' * 12}\n"
    f"👤 {hbold(line.name)}\n"
    f"💶 {hbold(line.price)}\n"
    f"{hbold('С:')} {hitalic(line.date_from)}\n"
    f"{hbold('До:')} {hitalic(line.date_to)}\n"
    f"{'➖' * 12}\n"
    "Что Вы хотите сделать?"
    )

    return text
def are_you_sure_to_delete_line_message(table_name, line): 
    text = (
        f"Выбрана строка таблицы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(line.name)}\n"
        f"💶 {hbold(line.price)}\n"
        f"{hbold('С:')} {hitalic(line.date_from)}\n"
        f"{hbold('До:')} {hitalic(line.date_to)}\n"
        f"{'➖' * 12}\n"
        "❔Вы уверены, что хотите удалить её?"
    )

    return text
def line_are_not_deleted_message(table_name, line):
    text = (
        f"Cтрока таблицы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(line.name)}\n"
        f"💶 {hbold(line.price)}\n"
        f"{hbold('С:')} {hitalic(line.date_from)}\n"
        f"{hbold('До:')} {hitalic(line.date_to)}\n"
        f"{'➖' * 12}\n"
        "❌ Не может быть удалена"
    )

    return text
def line_are_deleted_message(table_name, line):
    text = (
        f"Cтрока таблицы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(line.name)}\n"
        f"💶 {hbold(line.price)}\n"
        f"{hbold('С:')} {hitalic(line.date_from)}\n"
        f"{hbold('До:')} {hitalic(line.date_to)}\n"
        f"{'➖' * 12}\n"
        "✅ Удалена"
    )

    return text
def sent_name_message(table_name): return f"❔Добалвение данных\n{table_name_message(table_name)}\n\nОтправьте имя клиента (до 32 символов)"
def sent_price_message(table_name): return f"❔Добалвение данных\n{table_name_message(table_name)}\n\nОтправьте цену услуги (целое число)"
def sent_date_message(table_name): return f"❔Добалвение данных\n{table_name_message(table_name)}\n\nВведите в одном из форматов:\n 1) ddmmmYYYY-ddmmmYYYY \n 2) dd.mm.yyyy-dd.mm.yyyy\n\nДаты должны быть корректны."
def data_added_message(table_name, name, price, date): return f'💾✅ Данные добавлены в таблицу «{table_name}»\n\nКлиент: {name}\nЦена: {price}\nДаты: с {date[0]} по {date[1]}'
def line_name_changed_successfully_message(name, current_name): return f"✅ Имя «{current_name}» изменено.\n\n{current_name} > {name}"
def line_name_not_changed_message(current_name): return f"❌ Ошибка при измении имени «{current_name}»"
def line_price_changed_successfully_message(price, current_price): return f"✅ Цена «{current_price}» изменена.\n\n{current_price} > {price}"
def line_price_not_changed_message(current_price): return f"❌ Ошибка при измении цены «{current_price}»"
def line_date_changed_successfully_message(date, current_date): return f"✅ Дата «{current_date}» изменена.\n\n{current_date} > {date}"
def line_date_not_changed_message(current_date): return f"❌ Ошибка при измении даты «{current_date}»."
def all_table_lines_message(lines, table_name):
    text = "\n".join(
        f"👤 {hitalic(line.name)}\n"
        f"💶 {hitalic(line.price)}\n"
        f"{hbold('С:')} {hitalic(line.date_from)}\n"
        f"{hbold('До:')} {hitalic(line.date_to)}\n"
        f"{'➖' * 12}"
        for line in lines
    )
    return f"{hbold('Таблица:')} «{hitalic(table_name)}»\n{hbold('Клиентов:')} {hitalic(len(lines))}\n{'➖' * 12}\n{text}"
impossible_to_edit_line_message = "❌ Невозможно изменить эту строку"
pick_line_for_edit_message = "Выберите строку, которую хотите изменить"
def enter_new_price_message(name, table_name): return f'{table_name_message(table_name)}\nУкажите новую цену услуги для клиента {name}.'
def enter_new_name_message(name, table_name): return f'{table_name_message(table_name)}\nУкажите новое имя для клиента {name}.'
def enter_new_date_to_message(name, table_name): return f'{table_name_message(table_name)}\nУкажите новую дату "до" для клиента {name}.'
def enter_new_date_from_message(name, table_name): return f'{table_name_message(table_name)}\nУкажите новую дату "c" для клиента {name}.'