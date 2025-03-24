from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.templates.admin_templates.keyboards_templates import cancel_text, no_text, yes_text

cancel_delete_last_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=cancel_text, callback_data="delete_last_message")],
    ]
)


async def yes_or_not_delete_connection_keyboard(connection_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=yes_text, callback_data=f"delete_client_{connection_id}"
                ),
                InlineKeyboardButton(
                    text=no_text, callback_data="delete_last_message"
                ),
            ],
        ]
    )
