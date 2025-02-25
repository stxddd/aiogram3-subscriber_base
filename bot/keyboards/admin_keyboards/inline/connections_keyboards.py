from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.connections.dao import ConnectionDAO
from bot.templates.admin_templates.keyboards_templates import (
    cancel_text,
    connection_line_text,
    forward_text,
    back_text,
    page_num,
    get_marzban_link_text
)



async def get_connections_to_edit(client_id: int, page: int = 1, per_page: int = 3):
    connections = await ConnectionDAO.find_all(client_id=client_id)
    total_connections = len(connections)
    total_pages = (total_connections + per_page - 1) // per_page 

    start = (page - 1) * per_page
    end = start + per_page
    connection_page = connections[start:end]

    keyboard = InlineKeyboardBuilder()

    for connection in connection_page:
        
        keyboard.row(
            InlineKeyboardButton(
                text=connection_line_text(connection),
                callback_data=f"get_connection_to_edit_{connection.id}",
            )
        )

    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text=back_text,
                callback_data=f"edit_connections_page_{client_id}_{page - 1}"
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
                callback_data=f"edit_connections_page_{client_id}_{page + 1}"
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

async def get_connection_info_keyboard(connection_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_marzban_link_text,
                    callback_data=f"get_marzban_link_{connection_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=cancel_text, callback_data="delete_last_message"
                )
            ],
        ]
    )
