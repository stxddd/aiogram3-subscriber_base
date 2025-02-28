


from bot.utils.data_processing.date_converter import format_date


my_tables_text = "🪧 Базы"
create_table_text = "➕ Добавить базу"

back_text = "Назад"
cancel_text = "Отмена"

download_text = "Скачать"

look_all_text = "Посмотреть"
delete_client_text = "Удалить клиента"
delete_table_text = "Удалить базу"
change_table_name_text = "Переименовать"


paid_text = "Оплатил ✅"
didnt_pay_text = "Не оплатил ❌"

yes_text = "ДА"
no_text = "НЕТ"

forward_text = 'Вперед ➡'
back_text = '⬅ Назад'

def get_clients_for_edit_text(client_name, connections_count):
    return f"👤 {client_name} | 📡 {connections_count}"


def page_num(page, total_pages): return f"Страница {page}/{total_pages}"

accept_text = "✅ Принять"
reject_text = "❌ Отклонить"

get_marzban_link_text = '🔗 Ключ'
extend_text = '🔄 Продлить'

def connection_line_text(connection):
    return f"📡 {connection.os_name} | {format_date(connection.date_to)} | {connection.price}"

mailing_text = "📧 Рассылка"
searching_text = "🔍 Поиск"