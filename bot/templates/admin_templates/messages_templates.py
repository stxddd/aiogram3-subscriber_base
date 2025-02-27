from aiogram.utils.markdown import hbold, hitalic

from bot.utils.data_processing.date_converter import format_date

admin_welcome_message = "Привет!🤖 \n\n✅ Данный Бот поможет содержать базу клиентов Вашего прокси-сервера."
action_is_cancel_text = "❌ Действие отменено."

enter_table_name_message = "❔Введите название Базы (до 32 символов)."
pick_table_for_download_message = "❔Выберите таблицу, которую хотите скачать."
our_tables_message = "✅ Ваши Базы"
table_are_missing_message = "❌ В настоящие время у Вас нет таблиц."


def are_you_sure_to_delete_table_message(table_name):
    return f"❔ Вы уверены, что хотите удалить таблицу «{table_name}»?"


def table_are_deleted_message(table_name):
    return f"✅ База «{table_name}» удалена!"


def table_are_not_deleted_message(table_name):
    return f"❌ Невозможно удалить таблицу «{table_name}»!"

def enter_new_table_name_message(table_name):
    return f"❔ Введите новое имя для Базы «{table_name}» (до 32 символов)"

def table_name_message(table_name) -> str:
    return f"✅ База «{table_name}»"

def table_has_been_created_message(table_name):
    return f"💾✅ Создана База «{table_name}»"

def table_name_changed_successfully_message(table_name, current_table_name):
    return f"✅ База «{current_table_name}» переименована.\n\n{current_table_name} > {table_name}"

def table_has_no_clients_message(table_name):
    return f"❌ В базе «{table_name}» нет данных!"

def one_client_message(client, table_name, connections):
    text = (
        f"Выбран клиент Базы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.username)} \n📡 {len(connections)}\n"
    )

    text += f"{'➖' * 12}\n" "Список его подключений:"

    return text


def are_you_sure_to_delete_client_message(table_name, client, connections):
    text = (
        f"Выбран клиент Базы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.username)} \n📡 {len(connections)}\n"
    )

    text += f"{'➖' * 12}\n" "❔Вы уверены, что хотите удалить его?"

    return text


def client_are_not_deleted_message(table_name, client, connections):
    text = (
        f"Клиент Базы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.username)} \n📡{len(connections)}\n"
    )

    text += f"{'➖' * 12}\n" "❌ Не может быть удалён"

    return text


def client_are_deleted_message(table_name, client, connections):
    text = (
        f"Клиент Базы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.username)} \n📡{len(connections)}\n"
    )

    text += f"{'➖' * 12}\n" "✅ Удален"

    return text

def table_base_info_message(table_name, clients_count, all_prices):
    return f"{table_name_message(table_name)}\n\nКлиентов: {clients_count}\nОбщий доход: {all_prices}"


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

client_dose_not_have_connections_message ='❌ У клиента нет подключений'

def client_info_message(username, connections_count): return f'👤 {username} | 📡 {connections_count}'

def connection_info_message(connection, client_username): return f'👤 {client_username}\n\n{connection.os_name} | {connection.price} | {format_date(connection.date_to)}'

def link_message(connection, username): return f'🔗 Ссылка для подключения @{username}:\n\n `{connection.marzban_link}`\n\n{connection.price}₽\n{format_date(connection.date_to)}'