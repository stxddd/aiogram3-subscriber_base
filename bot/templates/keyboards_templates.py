from bot.utils.data_processing.date_converter import format_date


my_tables_text = "Мои таблицы"
create_table_text = "Создать таблицу"

back_text = "Назад"
cancel_text = "Отмена"

download_text = "Скачать"
edit_text = "Редактировать"
add_data_text = "Добавить данные"
look_all_text = "Посмотреть"
delete_line_text = "Удалить строку"
delete_table_text = "Удалить таблицу"
change_table_name_text = "Имя таблицы"
change_table_data_text = "Содержимое"
change_name_text = "Изменить имя клиента"
change_price_text = "Изменить цену"
change_date_to_text = "Изменить дату конца"
change_date_from_text = "Изменить дату начала"
table_statistic_text = "Статистика"
clients_for_some_period_text = "Клиенты на определённый период"

paid_text = "Оплатил ✅"
didnt_pay_text = "Не оплатил ❌"

yes_text = "ДА"
no_text = "НЕТ"

forward_text = 'Вперед ➡'
back_text = '⬅ Назад'

def get_lines_for_edit_text(client_name, client_days_late, client_date_to):
    line = f"👤 {client_name} | По {format_date(client_date_to)}"
    if client_days_late != 0:
        line += f" | ⚠ {client_days_late}"
    return line


def page_num(page, total_pages): return f"Страница {page}/{total_pages}"