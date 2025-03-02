from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.templates.admin_templates.keyboards_templates import (
    paid_text,
    cancel_text,
)


async def get_check_pay_keyboard(
    connection_id: int, new_price: int, new_months: int, key: int
):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=paid_text,
                    callback_data=f"extend_payment_check_completed_{connection_id}_{new_months}_{new_price}_{key}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=cancel_text, callback_data="delete_last_message"
                )
            ],
        ]
    )


async def get_check_pay_connect_keyboard(connection_id, key: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=paid_text,
                    callback_data=f"accept_connect_payment_check_completed_{connection_id}_{key}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=cancel_text, callback_data="delete_last_message"
                )
            ],
        ]
    )
