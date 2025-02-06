import re

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database.tables.clients.dao import ClientDAO
from bot.database.tables.dao import TableDAO
from bot.keyboards.reply.main_keyboards import main_keyboard
from bot.templates.errors_templates import (
    client_does_not_exists_error,
    invalid_date_format_error,
    table_dose_not_exists_error,
)
from bot.templates.messages_templates import (
    enter_new_date_to_message,
    line_date_changed_successfully_message,
    line_date_not_changed_message,
)

from bot.utils.data_processing.date_converter import parse_date
from bot.utils.data_processing.validators import is_valid_date, is_correct_date_part

router = Router()

EDIT_DATE_TO_PATTERN = r"^edit_data_date_to_(\d+)$"


class Form(StatesGroup):
    waiting_for_data_new_date_to = State()


@router.callback_query(F.data.regexp(EDIT_DATE_TO_PATTERN))
async def handle_edit_data_date_to(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(EDIT_DATE_TO_PATTERN, callback.data)
    client_id = int(match.group(1))

    current_client = await ClientDAO.find_by_id(client_id)
    if not current_client:
        return await callback.message.answer(client_does_not_exists_error)

    table = await TableDAO.find_one_or_none(id=current_client.table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    await state.update_data(client_id=client_id, table_name=table_name)
    await state.set_state(Form.waiting_for_data_new_date_to)

    await callback.message.answer(
        enter_new_date_to_message(table_name=table_name, name=current_client.name)
    )


@router.message(StateFilter(Form.waiting_for_data_new_date_to))
async def handle_line_date_to(message: Message, state: FSMContext):

    new_date_to = message.text.strip()

    if not is_correct_date_part(new_date_to):
        return await message.answer(invalid_date_format_error)

    data = await state.get_data()
    client_id = data.get("client_id")
    current_client = await ClientDAO.find_by_id(client_id)

    if not current_client:
        return await message.answer(client_does_not_exists_error)

    date_to_validate = is_valid_date(
        f"{current_client.date_from}.{(parse_date(new_date_to))}"
    )

    current_date_to = current_client.date_to
    if not date_to_validate:
        return await message.answer(invalid_date_format_error)

    updated_client = await ClientDAO.update(model_id=client_id, date_to=date_to_validate[1])
    if not updated_client:
        return await message.answer(
            line_date_not_changed_message(current_date=date_to_validate[1])
        )
    
    return await message.answer(
        line_date_changed_successfully_message(
            date=date_to_validate[1], current_date=current_date_to
        ),
        reply_markup=main_keyboard,
    )
