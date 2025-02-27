from bot.utils.data_processing.date_converter import format_date


adding_data_error = "❌ Произошла ошибка при добавлении данных."
name_so_long_error = "❌ Имя слишком длинное. Введите не более 32 символов."

imposible_to_create_table_error = "❌ Невозможно создать базу."
table_dose_not_exists_error = "❌ Такой Базы не существует."
connections_dose_not_exists_error = "❌ У вас ещё нет подключений."
connection_dose_not_exists_error = "❌ Такого подключения не существует."

def table_edit_error(table_name):
    return f"❌ Ошибка при изменении имени Базы «{table_name}»"


def table_name_not_changed_error(table_name):
    return f"❌ Ошибка при изменении имени Базы «{table_name}»"


def excel_table_can_not_create_error(table_name):
    return f"❌ Ошибка при формировании Базы «{table_name}»"


table_already_exists_error = (
    "❌ База с таким названием уже существует. Введите заново."
)

client_does_not_exists_error = "❌ Такого клиента не существует."
clients_does_not_exists_error = "❌ База пуста."

def client_name_not_changed_message(current_name):
    return f"❌ Ошибка при изменении имени «{current_name}»"

def client_price_not_changed_message(current_price):
    return f"❌ Ошибка при изменении цены «{current_price}»"

def client_date_not_changed_message(current_date):
    return f"❌ Ошибка при изменении даты «{format_date(current_date)}»."

marzban_user_add_error = '❌ Ошибка при создании ключа доступа. Попробуйте еще раз.'
marzban_link_get_error = "❌ Ошибка при выдаче ключа доступа. Попробуйте еще раз."
