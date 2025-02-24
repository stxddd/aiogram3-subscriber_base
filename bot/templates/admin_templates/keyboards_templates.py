


my_tables_text = "🪧 Базы"
create_table_text = "➕ Добавить базу"

back_text = "Назад"
cancel_text = "Отмена"

download_text = "Скачать"
add_data_text = "Добавить клиента"
look_all_text = "Посмотреть"
delete_client_text = "Удалить клиента"
delete_table_text = "Удалить таблицу"
change_table_name_text = "Переименовать"
change_table_data_text = "Содержимое"
change_name_text = "Изменить имя клиента"
change_price_text = "Изменить цену"
change_date_to_text = "Изменить дату конца"
change_date_from_text = "Изменить дату начала"
clients_for_some_period_text = "Клиенты на определённый период"

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
