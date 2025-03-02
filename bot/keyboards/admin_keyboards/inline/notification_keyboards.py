from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.templates.admin_templates.keyboards_templates import(
    didnt_pay_text, 
    paid_text,
    accept_text,
    reject_text,
    cancel_text,
    send_text
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
    
    
async def confirm_sending_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=send_text, callback_data=f"send_message"),
                InlineKeyboardButton(text=cancel_text, callback_data=f"delete_last_message")
            ]
        ]
    )


async def extend_connection_keyboard(connection_id: int,months: int, price: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=accept_text, callback_data=f"accept_extend_{connection_id}_{months}_{price}"),
                InlineKeyboardButton(text=reject_text, callback_data=f"reject_extend_{connection_id}")
            ]
        ]
    )
