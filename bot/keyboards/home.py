from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.templates.keyboards import create_table_text, my_tables_text

home_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [(InlineKeyboardButton(text=my_tables_text, callback_data="get_tables"))],
        [(InlineKeyboardButton(text=create_table_text, callback_data="create_table"))],
    ]
)

