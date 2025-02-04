import re
from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.utils.validators import is_valid_date, is_valid_date_part
from bot.keyboards.reply.main_keyboards import main_keyboard
from bot.templates.errors_templates import invalid_date_format_error, client_dose_not_exists_error
from bot.templates.messages_templates import (
    line_date_changed_successfully_message,
    line_date_not_changed_message,
    enter_new_date_from_message
)
from bot.database.tables.clients.dao import ClientDAO
from bot.utils.date_converter import convert_to_short_format, get_date_for_db

router = Router()

EDIT_DATE_FROM_PATTERN = r"^edit_data_date_from_(\d+)_(.+)$"


class Form(StatesGroup):
    waiting_for_data_new_date_from = State()


@router.callback_query(F.data.regexp(EDIT_DATE_FROM_PATTERN))
async def handle_edit_data_date_from(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(EDIT_DATE_FROM_PATTERN, callback.data)
    line_id = int(match.group(1))
    table_name = match.group(2)

    current_line = await ClientDAO.find_one_or_none(id=line_id)
    if not current_line:
        return await callback.message.answer(client_dose_not_exists_error)

    await state.update_data(line_id=line_id, table_name=table_name)
    await state.set_state(Form.waiting_for_data_new_date_from)

    await callback.message.answer(
        enter_new_date_from_message(table_name=table_name, name=current_line.name)
    )


@router.message(StateFilter(Form.waiting_for_data_new_date_from))
async def handle_line_date_from(message: Message, state: FSMContext):
    new_date_from = message.text.strip()

    if not is_valid_date_part(new_date_from):
        return await message.answer(invalid_date_format_error)

    new_date_from = get_date_for_db(new_date_from)

    data = await state.get_data()
    line_id = data.get("line_id")

    current_client = await ClientDAO.find_by_id(line_id)
    if not current_client:
        return await message.answer(client_dose_not_exists_error)

    current_date_from = current_client.date_from

    date_to_validate = convert_to_short_format(f'{new_date_from}-{current_client.date_to}')

    if not date_to_validate or not is_valid_date(date_to_validate):
        return await message.answer(line_date_not_changed_message(current_date=current_date_from))
    
    updated_client = await ClientDAO.update(model_id=line_id, date_from=new_date_from)
    if updated_client:
        return await message.answer(
            line_date_changed_successfully_message(date=new_date_from, current_date=current_date_from),
            reply_markup=main_keyboard
        )

    return await message.answer(line_date_not_changed_message(current_date=current_date_from))