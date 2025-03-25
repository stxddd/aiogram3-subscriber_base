from aiogram.utils.markdown import hbold

from bot.utils.data_processing.date_converter import format_date


admin_welcome_message = "Привет!🤖 \n\n✅ Данный Бот поможет содержать базу клиентов Вашего сервера."
action_is_cancel_text = "❌ Действие отменено."
def table_name_message() -> str:
    return f"✅ Действия"
def table_name_changed_successfully_message(table_name, current_table_name):
    return f"✅ База «{current_table_name}» переименована.\n\n{current_table_name} > {table_name}"
def table_base_info_message(clients_count):
    return f"Клиентов: {clients_count}"
def one_client_message(client, connections):
    text = (
        f"Выбран клиент\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.tg_id)} \n📡 {len(connections)}\n"
    )
    text += f"{'➖' * 12}\n" 
    return text
def are_you_sure_to_delete_connection_message(client, connection):
    text = (
        f"Подключение:\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.tg_id)}\n\n{connection.os_name}\n{connection.price}\n{connection.date_to}\n"
    )
    text += f"{'➖' * 12}\n" "❔Вы уверены, что хотите удалить его?"
    return text
def client_are_not_deleted_message(client, connection):
    text = (
        f"Подключение:\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.tg_id)}\n\n{connection.os_name}\n{connection.price}\n{connection.date_to}\n"
    )

    text += f"{'➖' * 12}\n" "❌ Не может быть удалён"
    return text
def client_are_deleted_message(client, connection):
    text = (
        f"Подключение:\n"
        f"{'➖' * 12}\n"
        f"👤 {hbold(client.tg_id)}\n\n{connection.os_name}\n{connection.price}\n{connection.date_to}\n"
    )
    text += f"{'➖' * 12}\n" "✅ Удален"
    return text
def successful_extension_message(username, connection, new_date_to, old_date_to, old_price, new_price): return f"✅ Подключение продленно.\n\n{connection.os_name} | {old_price if old_price == new_price else str(old_price) + ' -> ' + str(new_price)} | {format_date(old_date_to)}\n\nДо {format_date(new_date_to)}"
client_dose_not_have_connections_message = '❌ У Вас нет подключений'
def client_info_message(username, connections_count): return f'👤 {username} | 📡 {connections_count}'
def connection_info_message(connection, client_username): return f'👤 {client_username}\n\n{connection.os_name} | {connection.price} | {format_date(connection.date_to)}'
def link_message(connection): return f'🔗 Ссылка для подключения {connection.os_name}:\n\n `{connection.marzban_link}`\n\nИстекает: {format_date(connection.date_to)}'
enter_message_for_mailing_message = "❔ Введите текст сообщения для рассылки."
enter_query_text_message = "❔ Введите Username или TgID для поиска клиента."
clients_by_query_are_missing_message = "❌ Клиентов по такому запросу нет."
def clients_by_query_message(query, length): return f"✅ Клиентов по запросу {query}: {length}"
def enter_code_for_delete_table(table_name):
    return f"❔ Введите код для удаления базы «{table_name}»"
def enter_code_for_delete_client(client, connection):
    return f"❔ Введите код для удаления 👤 {hbold(client.tg_id)}\n\n{connection.os_name}\n{connection.price}\n{connection.date_to}\n"
incorrect_code_message = "❌ Неверный код!"
def are_you_sure_to_send_mailing_message(message): return f"❔ Вы уверены, что хотите отправить сообщение?\n\n{message}"
def refunded_succsses_message(transaction_id): return f"✅ Звезды по операции \n\n{transaction_id}\n\nвозвращены! "
