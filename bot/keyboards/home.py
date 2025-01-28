from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.templates.keyboards import create_table, my_tables

home_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [(InlineKeyboardButton(text=my_tables, callback_data="get_tables"))],
        [(InlineKeyboardButton(text=create_table, callback_data="create_table"))],
    ]
)

delete_last_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [(InlineKeyboardButton(text="Отмена", callback_data="delete_last_message"))],
    ]
)
