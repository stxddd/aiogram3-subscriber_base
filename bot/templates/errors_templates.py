from bot.config import settings

table_limit = settings.MAX_TABLE_LIMIT
clients_limit = settings.MAX_CLIENT_LIMIT

adding_data_error = "❌ Произошла ошибка при добавлении данных."
name_so_long_error = "❌ Имя слишком длинное. Введите не более 32 символов."

imposible_to_create_table_error = "❌ Невозможно создать таблицу."
table_dose_not_exists_error = "❌ Такой таблицы не существует."


def table_edit_error(table_name):
    return f"❌ Ошибка при изменении имени таблицы «{table_name}»"


def table_name_not_changed_error(table_name):
    return f"❌ Ошибка при изменении имени таблицы «{table_name}»"


exceeded_the_limit_on_the_table_error = f"❌ У вас достигнут лимит таблиц. {table_limit}/{table_limit}"
exceeded_the_limit_on_the_table_download_error = (
    "❌ На сегодня Вы достигли лимита скачиваний. 5/5"
)


def excel_table_can_not_create_error(table_name):
    return f"❌ Ошибка при формировании таблицы «{table_name}»"


table_already_exists_error = (
    "❌ Таблица с таким названием уже существует. Введите заново."
)
price_must_be_int_error = "❌ Цена должна быть целым числом. Попробуйте снова."
invalid_date_format_error = "❌ Неверная дата.\n\nВведите в одном из форматов:\n1) ddmmmYYYY-ddmmmYYYY \n2) dd.mm.yyyy-dd.mm.yyyy\n\nПроверьте, чтобы даты были корректны и введите заново."
exceeded_the_limit_on_the_line_error = f"❌ У вас достигнут лимит клиентов в одной таблице. {clients_limit}/{clients_limit}"
client_does_not_exists_error = "❌ Такого клиента не существует."
clients_does_not_exists_error = "❌ Таблица пуста."
