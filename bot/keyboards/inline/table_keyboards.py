from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.tables.dao import TableDAO
from bot.templates.keyboards_templates import (
    add_data_text,
    cancel_text,
    change_table_name_text,
    delete_table_text,
    download_text,
    look_all_text,
)


async def get_my_tables_keyboard(user_tg_id: int):
    tables = await TableDAO.find_all(user_tg_id=user_tg_id)
    keyboard = InlineKeyboardBuilder()

    for table in tables:
        keyboard.add(
            InlineKeyboardButton(text=table.name, callback_data=f"get_{table.id}_table")
        )

    return keyboard.adjust(1).as_markup()


async def get_actions_with_table_keyboard(table_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=add_data_text, callback_data=f"add_client_{table_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=look_all_text, callback_data=f"edit_client_{table_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=download_text, callback_data=f"download_table_{table_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=change_table_name_text, callback_data=f"edit_name_{table_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=delete_table_text,
                    callback_data=f"prepare_to_delete_table_{table_id}",
                )
            ],
        ]
    )


async def get_edit_actions_with_table_keyboard(table_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=change_table_name_text, callback_data=f"edit_name_{table_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=cancel_text, callback_data=f"delete_last_message"
                )
            ],
        ]
    )
