from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.tables.clients.dao import ClientDAO
from bot.templates.admin_templates.keyboards_templates import (
    cancel_text,
    change_date_from_text,
    change_date_to_text,
    change_name_text,
    change_price_text,
    delete_client_text,
    get_clients_for_edit_text,
    forward_text,
    back_text,
    page_num,
)


async def get_clients_for_edit(table_id: int, page: int = 1, per_page: int = 10):
    clients = await ClientDAO.find_all_order_by(table_id=table_id)
    total_clients = len(clients)
    total_pages = (total_clients + per_page - 1) // per_page 

    start = (page - 1) * per_page
    end = start + per_page
    clients_page = clients[start:end]

    keyboard = InlineKeyboardBuilder()

    for client in clients_page:
        keyboard.row(
            InlineKeyboardButton(
                text=get_clients_for_edit_text(
                    client_name=client.name,
                    client_days_late=client.days_late,
                    client_date_to=client.date_to,
                ),
                callback_data=f"get_client_to_edit_{client.id}",
            )
        )

    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text=back_text,
                callback_data=f"edit_page_{table_id}_{page - 1}"
            )
        )
    
    nav_buttons.append(
        InlineKeyboardButton(
            text=page_num(page, total_pages),
            callback_data="noop"  
        )
    )
    
    if page < total_pages:
        nav_buttons.append(
            InlineKeyboardButton(
                text=forward_text,
                callback_data=f"edit_page_{table_id}_{page + 1}"
            )
        )

    if nav_buttons:
        keyboard.row(*nav_buttons) 

    keyboard.row(
        InlineKeyboardButton(
            text=cancel_text,
            callback_data="delete_last_message"
        )
    )

    return keyboard.as_markup()


async def get_clients_data_unit_to_edit(client_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=change_name_text, callback_data=f"edit_client_name_{client_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=change_price_text, callback_data=f"edit_client_price_{client_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=change_date_to_text,
                    callback_data=f"edit_client_date_to_{client_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=change_date_from_text,
                    callback_data=f"edit_client_date_from_{client_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=delete_client_text,
                    callback_data=f"prepare_to_delete_client_{client_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=cancel_text, callback_data="delete_last_message"
                )
            ],
        ]
    )
