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
clients_for_some_period_text = "Клиенты на опредленный период"

paid_text = "Оплатил ✅"
didnt_pay_text = "Не оплатил ❌"

yes_text = "ДА"
no_text = "НЕТ"

def get_lines_for_edit_text(client_name, client_price, client_date_from, client_date_to): return f"👤{client_name} 💶{client_price}\n⌚️{format_date(client_date_from)} - {format_date(client_date_to)}"
