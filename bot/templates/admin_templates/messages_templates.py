from aiogram.utils.markdown import hbold, hitalic

from bot.utils.data_processing.date_converter import format_date

admin_welcome_message = "Привет!🤖 \n\n✅ Данный Бот поможет вести таблицу клиентов, которым Вы предоставили доступ на ограниченное время к своим услугам.\n\n🔔Вы будете получать уведомления, когда клиенту будет необходимо пополнить баланс.\n\n💾 В любой момент Вы можете скачать свою таблицу в формате excel, изменить ее, удалить."
action_is_cancel_text = "❌ Действие отменено."

enter_table_name_message = "❔Введите название таблицы (до 32 символов)."
pick_table_for_download_message = "❔Выберите таблицу, которую хотите скачать."
our_tables_message = "✅ Ваши таблицы"
table_are_missing_message = "❌ В настоящие время у Вас нет таблиц."


def are_you_sure_to_delete_table_message(table_name):
    return f"❔ Вы уверены, что хотите удалить таблицу «{table_name}»?"


def table_are_deleted_message(table_name):
    return f"✅ Таблица «{table_name}» удалена!"


def table_are_not_deleted_message(table_name):
    return f"❌ Невозможно удалить таблицу «{table_name}»!"


def select_an_action_for_the_table_message(table_name):
    return f"❔Выберите, что Вы хотите изменить в таблице «{table_name}»?"


def enter_new_table_name_message(table_name):
    return f"❔ Введите новое имя для таблицы «{table_name}» (до 32 символов)"


def table_name_message(table_name) -> str:
    return f"✅ Таблица «{table_name}»"


def table_has_been_created_message(table_name):
    return f"💾✅ Создана таблица «{table_name}»"


def table_has_no_clients_message(table_name):
    return f"✅ Записей в таблице «{table_name}» нет."


def table_name_changed_successfully_message(table_name, current_table_name):
    return f"✅ Таблица «{current_table_name}» переименована.\n\n{current_table_name} > {table_name}"


def table_has_no_clients_message(table_name):
    return f"❌ В таблице «{table_name}» нет данных!"


def table_base_info_message(table_name, clients_count, all_prices):
    return f"{table_name_message(table_name)}\n\nКлиентов: {clients_count}\nОбщий доход: {all_prices}"


def one_client_message(client, table_name, connections):
    text = (
        f"Выбран клиент таблицы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.username)} \n📡 {len(connections)}\n"
    )

    text += f"{'➖' * 12}\n" "Список его подключений:"

    return text


def are_you_sure_to_delete_client_message(table_name, client, connections):
    text = (
        f"Выбран клиент таблицы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.username)} \n📡 {len(connections)}\n"
    )

    text += f"{'➖' * 12}\n" "❔Вы уверены, что хотите удалить его?"

    return text


def client_are_not_deleted_message(table_name, client, connections):
    text = (
        f"Клиент таблицы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.username)} \n📡{len(connections)}\n"
    )

    text += f"{'➖' * 12}\n" "❌ Не может быть удалён"

    return text


def client_are_deleted_message(table_name, client, connections):
    text = (
        f"Клиент таблицы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.username)} \n📡{len(connections)}\n"
    )

    text += f"{'➖' * 12}\n" "✅ Удален"

    return text


def sent_name_message(table_name):
    return f"❔Добавление данных\n{table_name_message(table_name)}\n\nОтправьте имя клиента (до 32 символов)"


def sent_price_message(table_name):
    return f"❔Добавление данных\n{table_name_message(table_name)}\n\nОтправьте цену услуги (целое число)"


def sent_date_message(table_name):
    return f"❔Добавление данных\n{table_name_message(table_name)}\n\nВведите в одном из форматов:\n 1) ddmmmYYYY-ddmmmYYYY \n 2) dd.mm.yyyy-dd.mm.yyyy\n\nДаты должны быть корректны."


def data_added_message(table_name, name, price, date):
    return f"💾✅ Данные добавлены в таблицу «{table_name}»\n\nКлиент: {name}\nЦена: {price}\nДаты: с {format_date(date[0])} по {format_date(date[1])}"


def client_name_changed_successfully_message(name, current_name):
    return f"✅ Имя «{current_name}» изменено.\n\n{current_name} > {name}"



def client_price_changed_successfully_message(price, current_price):
    return f"✅ Цена «{current_price}» изменена.\n\n{current_price} > {price}"



def client_date_changed_successfully_message(date, current_date):
    return f"✅ Дата «{format_date(current_date)}» изменена.\n\n{format_date(current_date)} > {format_date(date)}"


impossible_to_edit_client_message = "❌ Невозможно изменить этого клиента"
pick_client_for_edit_message = "Выберите клиента, которого хотите изменить"


def enter_new_price_message(name, table_name):
    return f"{table_name_message(table_name)}\nУкажите новую цену услуги для клиента {name}."


def enter_new_name_message(name, table_name):
    return f"{table_name_message(table_name)}\nУкажите новое имя для клиента {name}."


def enter_new_date_to_message(name, table_name):
    return (
        f'{table_name_message(table_name)}\nУкажите новую дату конца для клиента {name}.'
    )


def enter_new_date_from_message(name, table_name):
    return (
        f'{table_name_message(table_name)}\nУкажите новую дату начала для клиента {name}.'
    )


def client_date_to_expired(client_name, date_to):
    return f"⚠ {client_name} | {format_date(date_to)} необходимо внести оплату!"


def payment_has_been_completed_message(client_name, client_date_from, client_date_to):
    return f"✅ Клиент {client_name} оплатил услуги. \n\n❔ Укажите новую дату окончания услуг \n\nПрошлые даты: c {format_date(client_date_from)} по {format_date(client_date_to)}"


def payment_didnt_completed_message(client_name, days_late):
    return f"❌ Клиент {client_name} не оплатил.\n\n⚠ Дней задержки: {days_late}"


anti_flood_message = "⛔ Вы слишком быстро отправляете сообщения! Подождите немного."

def request_to_connect_message(username, date_to): return f"✅ Новая заявка на подключение к серверу\n\n{username} | По: {format_date(date_to)}"

def marzban_user_added_message(username, date_to): return f"✅ Клиент {username} успешно подключен.\n\nПо: {format_date(date_to)}"

def marzban_user_rejected_message(username): return f"❌ Клиенту {username} отказано в доступе."

def pick_table_for_client_message(username): return f'✅ Выберите таблицу, для клиента @{username}'