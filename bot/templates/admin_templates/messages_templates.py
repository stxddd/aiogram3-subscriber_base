from aiogram.utils.markdown import hbold, hitalic

from bot.utils.data_processing.date_converter import format_date

admin_welcome_message = "Привет!🤖 \n\n✅ Данный Бот поможет содержать базу клиентов Вашего сервера."
action_is_cancel_text = "❌ Действие отменено."

enter_table_name_message = "❔Введите название Базы (до 32 символов)."
pick_table_for_download_message = "❔Выберите базу, которую хотите скачать."
our_tables_message = "✅ Ваши Базы"
table_are_missing_message = "❌ В настоящие время у Вас нет баз."


def are_you_sure_to_delete_table_message(table_name):
    return f"❔ Вы уверены, что хотите удалить базу «{table_name}»?"


def table_are_deleted_message(table_name):
    return f"✅ База «{table_name}» удалена!"


def table_are_not_deleted_message(table_name):
    return f"❌ Невозможно удалить базу «{table_name}»!"

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

def table_base_info_message(table_name, clients_count):
    return f"{table_name_message(table_name)}\n\nКлиентов: {clients_count}"


def one_client_message(client, table_name, connections):
    text = (
        f"Выбран клиент Базы «{hitalic(table_name)}»\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.username)} \n📡 {len(connections)}\n"
    )

    text += f"{'➖' * 12}\n" 

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

def client_date_to_expired(client_name, date_to):
    return f"⚠ {client_name} | {format_date(date_to)} необходимо внести оплату!"


def payment_has_been_completed_message(client_name, client_date_from, client_date_to):
    return f"✅ Клиент {client_name} оплатил услуги. \n\n❔ Укажите новую дату окончания услуг \n\nПрошлые даты: c {format_date(client_date_from)} по {format_date(client_date_to)}"


def payment_didnt_completed_message(client_name, days_late):
    return f"❌ Клиент {client_name} не оплатил.\n\n⚠ Дней задержки: {days_late}"


anti_flood_message = "⛔ Вы слишком быстро отправляете сообщения! Подождите немного."

def request_to_connect_message(username, connection, key): return f"✅ Новая заявка на подключение к серверу\n\n@{username} | {format_date(connection.date_to)} | {connection.price}\n\nКод: {key}"

def marzban_user_added_message(username, date_to): return f"✅ Клиент {username} успешно подключен.\n\nПо: {format_date(date_to)}"

def marzban_user_rejected_message(username): return f"❌ Клиенту {username} отказано в доступе."

def pick_table_for_client_message(username): return f'✅ Выберите базу, для клиента @{username}'

def client_dose_not_have_connections_message(username): return f'❌ У клиента @{username} нет подключений'

def client_info_message(username, connections_count): return f'👤 {username} | 📡 {connections_count}'

def connection_info_message(connection, client_username): return f'👤 {client_username}\n\n{connection.os_name} | {connection.price} | {format_date(connection.date_to)}'

def link_message(connection, username): return f'🔗 Ссылка для подключения @{username}:\n\n `{connection.marzban_link}`\n\n{connection.price}₽\n{format_date(connection.date_to)}'

enter_message_for_mailing_message = "❔ Введите текст сообщения для рассылки."
enter_query_text_message = "❔ Введите Username или TgID для поиска клиента."
clients_by_query_are_missing_message = "❌ Клиентов по такому запросу нет."
def clients_by_query_message(query, length): return f"✅ Клиентов по запросу {query}: {length}"

def enter_code_for_delete_table(table_name):
    return f"❔ Введите код для удаления базы «{table_name}»"

def enter_code_for_delete_client(client_name):
    return f"❔ Введите код для удаления @{client_name}"

incorrect_code_message = "❌ Неверный код!"

def are_you_sure_to_send_mailing_message(message): return f"❔ Вы уверены, что хотите отправить сообщение?\n\n{message}"

def client_wants_to_extend_message(username, connection, new_date_to, old_price, new_price, key): return f'⚠ Клиент @{username} хочет продлить\n\n {connection.os_name} | {old_price if old_price == new_price else str(old_price) + ' -> ' + str(new_price)} | {format_date(connection.date_to)}\n\nДо {format_date(new_date_to)} \n\nКод: {key}\n\nПродолжить?'

def successful_extension_message(username, connection, new_date_to, old_date_to, old_price, new_price): return f"✅ Вы успешно продлили подключение @{username}\n\n{connection.os_name} | {old_price if old_price == new_price else str(old_price) + ' -> ' + str(new_price)} | {format_date(old_date_to)}\n\nДо {format_date(new_date_to)}"

def successful_extension_admin_message(connection, username, new_date_to, old_date_to, old_price, new_price):return f"✅ Подключение @{username} продленно.\n\n{connection.os_name} | {old_price if old_price == new_price else str(old_price) + ' -> ' + str(new_price)} | {format_date(old_date_to)}\n\nДо {format_date(new_date_to)}"

def connection_successfuly_created(username, connection): return f'✅ Клиент @{username} успешно подключен\n\n{connection.os_name} | {connection.date_to} | {connection.price}'