from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.tables.dao import TableDAO
from bot.templates.keyboards import add_data_text, download_text, look_all_text

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
            [InlineKeyboardButton(text=add_data_text, callback_data=f"add_data_{table_id}_{table_name}")],
            [InlineKeyboardButton(text=look_all_text, callback_data=f"look_all_{table_id}_{table_name}")],
            [InlineKeyboardButton(text=download_text, callback_data=f"download_{table_id}_{table_name}")],
        ]
    )
