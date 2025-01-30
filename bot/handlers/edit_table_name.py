import re

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.keyboards.inline.utils import cancel_delete_last_keyboard
from bot.templates.errors import (
    name_so_long_error,
)
from bot.templates.messages import (
    enter_new_table_name,
    name_changed_successfully_message,
    name_not_changed_message
)
from bot.utils.excel_generator import ExcelCRUD

from bot.database.tables.dao import TableDAO

router = Router()


class Form(StatesGroup):
    waiting_for_new_table_name_data = State()

def is_valid_name(name: str) -> bool:
    return len(name) <= 32


@router.callback_query(F.data.regexp(r"^edit_name_(\d+)_(.+)$"))
async def handle_add_line_to_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    match = re.match(r"^edit_name_(\d+)_(.+)$", callback.data)

    table_id = int(match.group(1))
    table_name = match.group(2)

    message_sent = await callback.message.answer(enter_new_table_name(table_name), reply_markup=cancel_delete_last_keyboard)

    await state.update_data(table_id=table_id, table_name=table_name, message_sent_id_name=message_sent.message_id)
    await state.set_state(Form.waiting_for_new_table_name_data)

@router.message(StateFilter(Form.waiting_for_new_table_name_data))
async def handle_line_name(message: Message, state: FSMContext):
    new_table_name = message.text.strip()
    tg_id = message.from_user.id

    if not is_valid_name(new_table_name):
        return await message.answer(name_so_long_error)

    data = await state.get_data()
    table_name = data.get("table_name")
    table_id = data.get("table_id")

    current_table = await TableDAO.find_by_id(table_id)

    if current_table:
        updated_table = await TableDAO.update(model_id=table_id, name=new_table_name)

        if updated_table:
            update_excel_file = await ExcelCRUD.rename_excel_table(
                table_id=table_id,
                new_table_name=new_table_name,
                table_name=table_name,
                tg_id=tg_id)
            return await message.answer(name_changed_successfully_message(table_name=new_table_name, old_table_name=table_name))

    return message.answer(name_not_changed_message(table_name=new_table_name))