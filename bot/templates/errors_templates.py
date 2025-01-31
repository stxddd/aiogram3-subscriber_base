#base errors
adding_data_error = "❌ Произошла ошибка при добавлении данных."
name_so_long_error='❌ Ошибка: имя слишком длинное. Введите не более 32 символов.'

#table errors
imposible_to_create_table_error = "❌ Ошибка: Невозможно создать таблицу."
table_dose_not_exists_error = "❌ Ошибка: такой таблицы не существует."
def table_edit_error(table_name): return f"❌ Ошибка при измении имени таблицы «{table_name}»"
def table_name_not_changed_error(table_name): return f"❌ Ошибка при измении имени таблицы «{table_name}»"
exceeded_the_limit_on_the_table_error = "❌ У вас достигнут лимит таблиц. 5/5"

#line errors
table_already_exists_error = "❌ Ошибка: таблица с такиим названием уже существует. Введите заново."
price_must_be_int_error = "❌ Ошибка: цена должна быть целым числом. Попробуйте снова."
invalid_date_format_error = "❌ Ошибка: неверный формат даты. Введите в формате dd.mm.yyyy-dd.mm.yyyy."
exceeded_the_limit_on_the_line_error = "❌ У вас достигнут лимит таблиц. 250/250"