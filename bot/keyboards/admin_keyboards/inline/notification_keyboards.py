from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.templates.admin_templates.keyboards_templates import(
    didnt_pay_text, 
    paid_text,
    accept_text,
    reject_text
) 


async def get_pay_info_keyboard(client_id: int):
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

async def get_marzban_access_keyboard(connection_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=accept_text, callback_data=f"accept_marzban_{connection_id}"),
                InlineKeyboardButton(text=reject_text, callback_data=f"reject_marzban_{connection_id}")
            ]
        ]
    )
