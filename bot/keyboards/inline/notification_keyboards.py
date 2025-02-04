from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.templates.keyboards_templates import didnt_pay_text, paid_text


async def get_pay_info(client_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=paid_text, callback_data=f"payment_completed_{client_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=didnt_pay_text,
                    callback_data=f"payment_didnt_completed_{client_id}",
                )
            ],
        ]
    )
