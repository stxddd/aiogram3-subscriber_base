from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.tables.dao import TableDAO
from bot.templates.keyboards import (
    add_data_text, 
    download_text, 
    look_all_text, 
    edit_text, 
    change_table_name_text,
    change_table_data_text,
    delete_text
)

async def get_my_tables_keyboard(owner_tg_id: int):

    tables = await TableDAO.find_all(owner_tg_id=owner_tg_id)
    keyboard = InlineKeyboardBuilder()

    for table in tables:
        keyboard.add(
            InlineKeyboardButton(
                text=table.name, callback_data=f"get_{table.id}_{table.name}_table"
            )
        )

    return keyboard.adjust(1).as_markup()

async def get_actions_with_table_keyboard(table_id: int, table_name: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=add_data_text, callback_data=f"add_data_to_table_{table_id}_{table_name}")],
            [InlineKeyboardButton(text=look_all_text, callback_data=f"look_all_table_data_{table_id}_{table_name}")],
            [InlineKeyboardButton(text=download_text, callback_data=f"download_table_{table_id}_{table_name}")],
            [InlineKeyboardButton(text=edit_text, callback_data=f"edit_table_{table_id}_{table_name}")],
            [InlineKeyboardButton(text=delete_text, callback_data=f"prepare_to_delete_table_{table_id}_{table_name}")],
        ]
    )

async def get_edit_actions_with_table_keyboard(table_id: int, table_name: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=change_table_name_text, callback_data=f"edit_name_{table_id}_{table_name}")],
            [InlineKeyboardButton(text=change_table_data_text, callback_data=f"edit_data_{table_id}_{table_name}")],
        ]
    )
