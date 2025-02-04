from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.templates.keyboards_templates import create_table_text, my_tables_text

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [(KeyboardButton(text=my_tables_text))],
        [(KeyboardButton(text=create_table_text))],
    ],
    resize_keyboard=True,
)
