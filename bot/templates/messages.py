from aiogram.utils.markdown import hbold, hitalic

welcome_message = "Привет!🤖 \n\n✅ Данный Бот поможет вести базу абонентов, которым Вы предоставили доступ на ограниченное время к своим услугам.\n\n🔔Вы будете получать уведомления, когда клиенту будет необходимо пополнить баланс.\n\n💾 В любой момент Вы можете запросить свою базу в формате excel, изменить ее, удалить."
enter_table_name_message = "Введите название таблицы"
data_format_message = "Чтобы добавить данные в таблицу отправьте их в следующем формате\n\ntable_id-Телеграм-Цена-мес1_год-мес2_год-день_оплаты"
pick_table_for_download_message = "Выберите таблицу, которую хотите скачать."
new_data_added_message = "💾✅ Данные добавлены в таблицу "
main_menu = "Вы находитесь в главном меню."
our_tables = "Все ваши таблицы"

sent_client_name_message = "Отправьте имя клиента (до 32 символов)"
sent_client_price_message = "Отправьте цену услуги (целое число)"
sent_client_date_message = "Отправьте даты оказания услуг в формате dd.mm.yyyy-dd.mm.yyyy"

def table_name_message(table_name) -> str: return f"Таблица: «{table_name}»"

def data_added_message(table_name, name, price, date): return f'{new_data_added_message}«{table_name}»\n\nКлиент: {name}\nЦена: {price}\nДаты: {date}'
def table_has_been_created_message(table_name): return f"💾✅ Создана таблица: «{table_name}»"
def table_has_no_lines_message(table_name): return f"Записей в таблице «{table_name}» нет."

def all_table_lines(lines, table_name):
    text = "\n".join(
            f"{hbold('Клиент')}: {hitalic(line.subscriber_tg_id)}\n"
            f"{hbold('Цена')}: {hitalic(line.subscriber_price)}\n"
            f"{hbold('Период')}: {line.subscriber_date}\n"
            f"{'-' * 20}"
            for line in lines
        )
    
    return f"Таблица: «{table_name}»\nКлиентов: {len(lines)}\n\n{text}"
    