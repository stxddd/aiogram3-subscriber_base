import re
from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.utils.validators import is_valid_name
from bot.keyboards.reply.main_keyboards import main_keyboard
from bot.templates.errors_templates import name_so_long_error, client_dose_not_exists_error
from bot.templates.messages_templates import (
    line_name_changed_successfully_message,
    line_name_not_changed_message,
    enter_new_name_message
)
from bot.database.tables.clients.dao import ClientDAO

router = Router()

EDIT_NAME_PATTERN = r"^edit_data_name_(\d+)_(.+)$"


class Form(StatesGroup):
    waiting_for_data_new_name = State()


@router.callback_query(F.data.regexp(EDIT_NAME_PATTERN))
async def handle_edit_data_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(EDIT_NAME_PATTERN, callback.data)
    line_id = int(match.group(1))
    table_name = match.group(2)

    current_line = await ClientDAO.find_one_or_none(id=line_id)
    if not current_line:
        return await callback.message.answer(client_dose_not_exists_error)

    await state.update_data(line_id=line_id, table_name=table_name)

    await callback.message.answer(
        enter_new_name_message(table_name=table_name, name=current_line.name)
    )
    await state.set_state(Form.waiting_for_data_new_name)


@router.message(StateFilter(Form.waiting_for_data_new_name))
async def handle_new_line_name(message: Message, state: FSMContext):
    new_name = message.text.strip()

    if not is_valid_name(new_name):
        return await message.answer(name_so_long_error)

    data = await state.get_data()
    line_id = data.get("line_id")

    current_line = await ClientDAO.find_by_id(line_id)
    if not current_line:
        return await message.answer(client_dose_not_exists_error)

    current_name = current_line.name

    updated_line = await ClientDAO.update(model_id=line_id, name=new_name)
    if updated_line:
        return await message.answer(
            line_name_changed_successfully_message(name=new_name, current_name=current_name),
            reply_markup=main_keyboard
        )

    return await message.answer(line_name_not_changed_message(current_name=current_name))
