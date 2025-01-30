from aiogram.utils.markdown import hbold, hitalic

welcome_message = "Привет!🤖 \n\n✅ Данный Бот поможет вести базу абонентов, которым Вы предоставили доступ на ограниченное время к своим услугам.\n\n🔔Вы будете получать уведомления, когда клиенту будет необходимо пополнить баланс.\n\n💾 В любой момент Вы можете запросить свою базу в формате excel, изменить ее, удалить."
enter_table_name_message = "❔Введите название таблицы (до 32 символов)."
data_format_message = "❔Чтобы добавить данные в таблицу отправьте их в следующем формате\n\ntable_id-Телеграм-Цена-мес1_год-мес2_год-день_оплаты"
pick_table_for_download_message = "❔Выберите таблицу, которую хотите скачать."
our_tables = "✅ Ваши таблицы"
table_are_missing_text = "❌ В настоящие время у Вас нет таблиц."

def sent_client_name_message(table_name): return f"❔Добалвение данных\n{table_name_message(table_name)}\n\nОтправьте имя клиента (до 32 символов)"
def sent_client_price_message(table_name): return f"❔Добалвение данных\n{table_name_message(table_name)}\n\nОтправьте цену услуги (целое число)"
def sent_client_date_message(table_name): return f"❔Добалвение данных\n{table_name_message(table_name)}\n\nОтправьте даты оказания услуг в формате dd.mm.yyyy-dd.mm.yyyy"

action_is_cancel_text = '❌ Действие отменено.'

def table_name_message(table_name) -> str: return f"✅ Таблица: «{table_name}»"
def data_added_message(table_name, name, price, date): return f'💾✅ Данные добавлены в таблицу «{table_name}»\n\nКлиент: {name}\nЦена: {price}\nДаты: {date}'
def table_has_been_created_message(table_name): return f"💾✅ Создана таблица: «{table_name}»"
def table_has_no_lines_message(table_name): return f"✅ Записей в таблице «{table_name}» нет."

def all_table_lines(lines, table_name):
    text = "\n".join(
        f"{hbold('Номер:')} {index + 1}\n"
        f"{hbold('👤')} {hitalic(line.subscriber_tg_id)}\n"
        f"{hbold('💶')} {hitalic(line.subscriber_price)}\n"
        f"{hbold('⌚️')} {line.subscriber_date}\n"
        f"{'➖' * 12}"
        for index, line in enumerate(lines)
    )
    return f"{hbold('Таблица:')} «{hitalic(table_name)}»\n{hbold('Клиентов:')} {hitalic(len(lines))}\n{'➖' * 12}\n{text}"