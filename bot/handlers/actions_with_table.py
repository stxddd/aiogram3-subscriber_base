import re
from pathlib import Path

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message

from bot.database.tables.lines.dao import LineDAO
from bot.keyboards.home import delete_last_keyboard, home_keyboard
from bot.keyboards.tables import actions_with_table_keyboard
from bot.templates.errors import adding_data_error, table_dose_not_exists_error
from bot.templates.messages import main_menu, new_data_added_message
from bot.utils.excel_generator import ExcelCRUD

router = Router()




@router.callback_query(F.data.regexp(r"^get_(\d+)_(.+?)_table$"))
async def actions_with_table(callback: CallbackQuery, state: FSMContext):
    match = re.match(r"^get_(\d+)_(.+?)_table$", callback.data)
    await callback.answer()

    table_id = int(match.group(1))
    table_name = match.group(2)

    await state.update_data(table_id=table_id, table_name=table_name)

    message_sent = await callback.message.edit_text(
        f"Таблица: «{table_name}»", reply_markup=actions_with_table_keyboard
    )

    await state.update_data(message_sent_id_actions_with_table=message_sent.message_id)



