from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.templates.keyboards import cancel_text


cancel_delete_last_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [(InlineKeyboardButton(text=cancel_text, callback_data="delete_last_message"))],
    ]
)
