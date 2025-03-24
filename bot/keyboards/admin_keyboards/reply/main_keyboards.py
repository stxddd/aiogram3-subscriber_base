from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from bot.templates.admin_templates.keyboards_templates import (
    my_clients_text,
    mailing_text,
    search_text,
)
from bot.templates.user_templates.keyboards_templates import (
    get_new_connection_text,
    get_instruction_text,
    my_connections_text,
)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=my_clients_text),
        ],
        [
            KeyboardButton(text=get_new_connection_text),
            KeyboardButton(text=my_connections_text),
        ],
        [KeyboardButton(text=get_instruction_text)],
        [KeyboardButton(text=mailing_text)],
        [KeyboardButton(text=search_text)],
    ],
    resize_keyboard=True,
)
