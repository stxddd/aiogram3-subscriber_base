from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.templates.user_templates.keyboards_templates import (
    get_new_connection_text,
    get_instruction_text,
    my_connections_text,
)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=get_new_connection_text)],
        [KeyboardButton(text=my_connections_text)],
        [KeyboardButton(text=get_instruction_text)],
    ],
    resize_keyboard=True,
)
