from aiogram.utils.markdown import hbold, hitalic

#base message
welcome_message = "Привет!🤖 \n\n✅ Данный Бот поможет вести базу абонентов, которым Вы предоставили доступ на ограниченное время к своим услугам.\n\n🔔Вы будете получать уведомления, когда клиенту будет необходимо пополнить баланс.\n\n💾 В любой момент Вы можете запросить свою базу в формате excel, изменить ее, удалить."
action_is_cancel_text = '❌ Действие отменено.'

#table messages
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
def table_name_changed_successfully_message(table_name, old_table_name): return f"✅ Таблица «{old_table_name}» переименована.\n\n{old_table_name} > {table_name}"
def table_has_no_lines_message(table_name): return f"❌ В таблице «{table_name}» нет данных!"

#line messages
def one_line_message(line, table_name):
    text = (
    f"Выбрана строка таблицы «{hitalic(table_name)}»\n"
    f"{'➖' * 12}\n"
    f"👤 {hbold(line.subscriber_tg_id)}\n"
    f"💶 {hbold(line.subscriber_price)}\n"
    f"⌚️ {hbold(line.subscriber_date)}\n"
    f"{'➖' * 12}\n"
    "Что Вы хотите сделать?"
    )

    return text
def are_you_sure_to_delete_line_message(table_name, line): 
    text = (
        f"Выбрана строка таблицы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(line.subscriber_tg_id)}\n"
        f"💶 {hbold(line.subscriber_price)}\n"
        f"⌚️ {hbold(line.subscriber_date)}\n"
        f"{'➖' * 12}\n"
        "❔Вы уверены, что хотите удалить её?"
    )

    return text
def line_are_not_deleted_message(table_name, line):
    text = (
        f"Cтрока таблицы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(line.subscriber_tg_id)}\n"
        f"💶 {hbold(line.subscriber_price)}\n"
        f"⌚️ {hbold(line.subscriber_date)}\n"
        f"{'➖' * 12}\n"
        "❌ Не может быть удалена"
    )

    return text
def line_are_deleted_message(table_name, line):
    text = (
        f"Cтрока таблицы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(line.subscriber_tg_id)}\n"
        f"💶 {hbold(line.subscriber_price)}\n"
        f"⌚️ {hbold(line.subscriber_date)}\n"
        f"{'➖' * 12}\n"
        "✅ Удалена"
    )

    return text
def sent_client_name_message(table_name): return f"❔Добалвение данных\n{table_name_message(table_name)}\n\nОтправьте имя клиента (до 32 символов)"
def sent_client_price_message(table_name): return f"❔Добалвение данных\n{table_name_message(table_name)}\n\nОтправьте цену услуги (целое число)"
def sent_client_date_message(table_name): return f"❔Добалвение данных\n{table_name_message(table_name)}\n\nВведите в одном из форматов:\n 1) ddmmmYYYY-ddmmmYYYY \n 2) dd.mm.yyyy-dd.mm.yyyy\n"
def data_added_message(table_name, name, price, date): return f'💾✅ Данные добавлены в таблицу «{table_name}»\n\nКлиент: {name}\nЦена: {price}\nДаты: {date}'
def line_client_name_changed_successfully_message(client_name, old_client_name): return f"✅ Имя «{old_client_name}» изменено.\n\n{old_client_name} > {client_name}"
def line_client_name_not_changed_message(old_client_name): return f"❌ Ошибка при измении имени «{old_client_name}»"
def line_client_price_changed_successfully_message(client_price, old_client_price): return f"✅ Цена «{old_client_price}» изменена.\n\n{old_client_price} > {client_price}"
def line_client_price_not_changed_message(old_client_price): return f"❌ Ошибка при измении цены «{old_client_price}»"
def line_client_date_changed_successfully_message(client_date, old_client_date): return f"✅ Дата «{old_client_date}» изменена.\n\n{old_client_date} > {client_date}"
def line_client_date_not_changed_message(old_client_date): return f"❌ Ошибка при измении даты «{old_client_date}»"
def all_table_lines_message(lines, table_name):

    text = "\n".join(
        f"👤 {hitalic(line.subscriber_tg_id)}\n"
        f"💶 {hitalic(line.subscriber_price)}\n"
        f"{hbold('С:')} {hitalic(line.subscriber_date.split('-')[0])}\n"
        f"{hbold('До:')} {hitalic(line.subscriber_date.split('-')[1])}\n"
        f"{'➖' * 12}"
        for index, line in enumerate(lines)
    )
    return f"{hbold('Таблица:')} «{hitalic(table_name)}»\n{hbold('Клиентов:')} {hitalic(len(lines))}\n{'➖' * 12}\n{text}"
impossible_to_edit_line_message = "❌ Невозможно изменить эту строку"
pick_line_for_edit_message = "Выберите строку, которую хотите изменить"
def enter_new_client_price_message(client_name, table_name): return f'{table_name_message(table_name)}\nУкажите новую цену услуги для клиента {client_name}.'
def enter_new_client_name_message(client_name, table_name): return f'{table_name_message(table_name)}\nУкажите новое имя для клиента {client_name}.'
def enter_new_client_date_message(client_name, table_name): return f'{table_name_message(table_name)}\nУкажите новые даты для клиента {client_name}.'