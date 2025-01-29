from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.tables.dao import TableDAO
from bot.templates.keyboards import back_text, add_data_text, download_text, look_all_text

async def get_my_tables_keyboard(owner_tg_id: int):

    tables = await TableDAO.find_all(owner_tg_id=owner_tg_id)
    keyboard = InlineKeyboardBuilder()

    for table in tables:
        keyboard.add(
            InlineKeyboardButton(
                text=table.name, callback_data=f"get_{table.id}_{table.name}_table"
            )
        )

    keyboard.add(InlineKeyboardButton(text=back_text, callback_data="main_menu"))
    return keyboard.adjust(1).as_markup()


actions_with_table_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [(InlineKeyboardButton(text=add_data_text, callback_data="add_data_to_table"))],
        [(InlineKeyboardButton(text=look_all_text, callback_data="look_all_lines"))],
        [(InlineKeyboardButton(text=download_text, callback_data="download_table"))],
        [(InlineKeyboardButton(text=back_text, callback_data="main_menu"))],
    ]
)