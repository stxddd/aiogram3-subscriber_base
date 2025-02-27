from bot.config import settings
from bot.utils.data_processing.date_converter import format_date

table_limit = settings.MAX_TABLE_LIMIT
clients_limit = settings.MAX_CLIENT_LIMIT

adding_data_error = "❌ Произошла ошибка при добавлении данных."
name_so_long_error = "❌ Имя слишком длинное. Введите не более 32 символов."

imposible_to_create_table_error = "❌ Невозможно создать таблицу."
table_dose_not_exists_error = "❌ Такой Базы не существует."
connections_dose_not_exists_error = "❌ У вас ещё нет подключений."

def table_edit_error(table_name):
    return f"❌ Ошибка при изменении имени Базы «{table_name}»"


def table_name_not_changed_error(table_name):
    return f"❌ Ошибка при изменении имени Базы «{table_name}»"


exceeded_the_limit_on_the_table_error = f"❌ У вас достигнут лимит таблиц. {table_limit}/{table_limit}"
exceeded_the_limit_on_the_table_download_error = (
    "❌ На сегодня Вы достигли лимита скачиваний. 5/5"
)


def excel_table_can_not_create_error(table_name):
    return f"❌ Ошибка при формировании Базы «{table_name}»"


table_already_exists_error = (
    "❌ База с таким названием уже существует. Введите заново."
)

exceeded_the_limit_on_the_client_error = f"❌ У вас достигнут лимит клиентов в одной базе. {clients_limit}/{clients_limit}"
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
