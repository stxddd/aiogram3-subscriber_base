from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.templates.admin_templates.keyboards_templates import (
    cancel_text,
    send_text,
)

async def confirm_sending_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=send_text, callback_data="send_message"
                ),
                InlineKeyboardButton(
                    text=cancel_text, callback_data="delete_last_message"
                ),
            ]
        ]
    )
