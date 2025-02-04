import re

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.utils.validators import is_valid_name
from bot.keyboards.reply.main_keyboards import main_keyboard
from bot.keyboards.inline.utils_keyboards import cancel_delete_last_keyboard
from bot.templates.errors_templates import (
    name_so_long_error,
    table_dose_not_exists_error
)
from bot.templates.messages_templates import (
    enter_new_table_name_message,
    table_name_changed_successfully_message,
)
from bot.database.tables.dao import TableDAO
from bot.templates.errors_templates import table_name_not_changed_error

router = Router()


class Form(StatesGroup):
    waiting_for_new_table_name_data = State()

EDIT_TABLE_NAME_PATTERN = r"^edit_name_(\d+)$"

@router.callback_query(F.data.regexp(EDIT_TABLE_NAME_PATTERN))
async def handle_add_line_to_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(EDIT_TABLE_NAME_PATTERN, callback.data)
    table_id = int(match.group(1))
    
    table = await TableDAO.find_one_or_none(id=table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    message_sent = await callback.message.answer(enter_new_table_name_message(table_name), reply_markup=cancel_delete_last_keyboard)

    await state.update_data(table_id=table_id, table_name=table_name, message_sent_id_name=message_sent.message_id)
    await state.set_state(Form.waiting_for_new_table_name_data)


@router.message(StateFilter(Form.waiting_for_new_table_name_data))
async def handle_table_name(message: Message, state: FSMContext):
    new_table_name = message.text.strip()

    if not is_valid_name(new_table_name):
        return await message.answer(name_so_long_error)

    data = await state.get_data()
    table_name = data.get("table_name")
    table_id = data.get("table_id")

    current_table = await TableDAO.find_by_id(table_id)

    if current_table:
        updated_table = await TableDAO.update(model_id=table_id, name=new_table_name)
        if updated_table:
            return await message.answer(table_name_changed_successfully_message(table_name=new_table_name, current_table_name=table_name), reply_markup = main_keyboard)

    return message.answer(table_name_not_changed_error(table_name=table_name))