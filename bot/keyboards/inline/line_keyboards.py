from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.tables.clients.dao import ClientDAO
from bot.templates.keyboards_templates import (
    cancel_text,
    change_date_from_text,
    change_date_to_text,
    change_name_text,
    change_price_text,
    delete_line_text,
    get_lines_for_edit_text
)


async def get_lines_for_edit(table_id: int):
    clients = await ClientDAO.find_all(table_id=table_id)

    keyboard = InlineKeyboardBuilder()

    for client in clients:
        keyboard.add(
            InlineKeyboardButton(
                text=get_lines_for_edit_text(client_name=client.name,
                                             client_price=client.price, 
                                             client_date_from=client.date_from, 
                                             client_date_to=client.date_to),
                callback_data=f"get_line_to_edit_{client.id}",
            )
        )

    keyboard.add(
        (InlineKeyboardButton(text=cancel_text, callback_data="delete_last_message"))
    )

    return keyboard.adjust(1).as_markup()


async def get_lines_data_unit_to_edit(client_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=change_name_text, callback_data=f"edit_data_name_{client_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=change_price_text, callback_data=f"edit_data_price_{client_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=change_date_to_text,
                    callback_data=f"edit_data_date_to_{client_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=change_date_from_text,
                    callback_data=f"edit_data_date_from_{client_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=delete_line_text,
                    callback_data=f"prepare_to_delete_line_{client_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=cancel_text, callback_data="delete_last_message"
                )
            ],
        ]
    )
