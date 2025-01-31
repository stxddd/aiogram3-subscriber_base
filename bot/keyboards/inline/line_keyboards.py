from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.tables.lines.dao import LineDAO
from bot.templates.keyboards_templates import (
    delete_line_text,
    change_client_name_text,
    change_client_price_text,
    change_client_date_text
)
from bot.templates.keyboards_templates import cancel_text


async def get_lines_for_edit(table_name: str, table_id: int):
    lines = await LineDAO.find_all(table_id=table_id)

    keyboard = InlineKeyboardBuilder()

    for line in lines:
        keyboard.add(
            InlineKeyboardButton(
                text=f'👤{line.subscriber_tg_id} 💶{line.subscriber_price}\n⌚️{line.subscriber_date}', callback_data=f"get_line_to_edit_{line.id}_{table_name}"
            )
        )

    keyboard.add((InlineKeyboardButton(text=cancel_text, callback_data="delete_last_message")))

    return keyboard.adjust(1).as_markup()


async def get_lines_data_unit_to_edit(line_id: int, table_name: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=change_client_name_text, callback_data=f"edit_data_name_{line_id}_{table_name}")],
            [InlineKeyboardButton(text=change_client_price_text, callback_data=f"edit_data_price_{line_id}_{table_name}")],
            [InlineKeyboardButton(text=change_client_date_text, callback_data=f"edit_data_date_{line_id}_{table_name}")],
            [InlineKeyboardButton(text=delete_line_text, callback_data=f"prepare_to_delete_line_{line_id}_{table_name}")],
            [InlineKeyboardButton(text=cancel_text, callback_data="delete_last_message")],
        ]
    )