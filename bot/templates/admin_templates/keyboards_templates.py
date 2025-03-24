from bot.utils.data_processing.date_converter import format_date

my_clients_text = "🪧 Клиенты"
mailing_text = "📧 Рассылка"
search_text  = "🔍 Поиск"

cancel_text = "Отмена"

download_text = "Скачать Excel"

look_all_text = "Все клиенты"

yes_text = 'Да'
no_text = 'Нет'

forward_text = "Вперед ➡"
back_text = "⬅ Назад"

def get_clients_for_edit_text(client_name, connections_count):
    return f"👤 {client_name} | 📡 {connections_count}"

def page_num(page, total_pages): return f"Страница {page}/{total_pages}"

accept_text = "✅ Принять"
reject_text = "❌ Отклонить"

get_marzban_link_text = '🔗 Ключ'
extend_text = '🔄 Продлить'
delete_text = "🗑 Удалить"
send_text = '📧 Отправить'

def connection_line_text(connection):
    return f"📡 {connection.os_name} | {format_date(connection.date_to)} | {connection.price}"
