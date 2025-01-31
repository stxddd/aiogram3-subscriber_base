from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.templates.keyboards_templates import my_tables_text, create_table_text

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [(KeyboardButton(text=my_tables_text))],
    [(KeyboardButton(text=create_table_text))],
], resize_keyboard=True)