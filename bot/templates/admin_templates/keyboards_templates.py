from bot.utils.data_processing.date_converter import format_date

my_tables_text = "🪧 Базы"
create_table_text = "➕ Добавить базу"
mailing_text = "📧 Рассылка"
search_text  = "🔍 Поиск"

cancel_text = "Отмена"

download_text = "Получить"

look_all_text = "Клиенты"
delete_client_text = "Удалить клиента"
delete_table_text = "Удалить базу"
change_table_name_text = "Переименовать"

paid_text = "Оплатил(а) ✅"
didnt_pay_text = "Не оплатил ❌"

yes_text = "ДА"
no_text = "НЕТ"

forward_text = "Вперед ➡"
back_text = "⬅ Назад"

def get_clients_for_edit_text(client_name, connections_count):
    return f"👤 {client_name} | 📡 {connections_count}"


def page_num(page, total_pages): return f"Страница {page}/{total_pages}"

accept_text = "✅ Принять"
reject_text = "❌ Отклонить"

get_marzban_link_text = '🔗 Ключ'
extend_text = '🔄 Продлить'

send_text = '📧 Отправить'

def connection_line_text(connection):
    return f"📡 {connection.os_name} | {format_date(connection.date_to)} | {connection.price}"
