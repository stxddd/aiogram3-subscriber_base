import re

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database.tables.clients.dao import ClientDAO
from bot.database.tables.dao import TableDAO
from bot.keyboards.admin_keyboards.reply.main_keyboards import main_keyboard
from bot.templates.admin_templates.errors_templates import (
    client_date_not_changed_message,
    client_does_not_exists_error,
    invalid_date_format_error,
    table_dose_not_exists_error,
    client_date_not_changed_message
)
from bot.templates.admin_templates.messages_templates import (
    client_date_changed_successfully_message,
    enter_new_date_from_message,
)
from bot.utils.data_processing.date_converter import parse_date
from bot.utils.data_processing.validators import is_valid_date, is_correct_date_part
from bot.decorators.admin_required import admin_required

router = Router()

EDIT_DATE_FROM_PATTERN = r"^edit_client_date_from_(\d+)$"


class Form(StatesGroup):
    waiting_for_data_new_date_from = State()


@router.callback_query(F.data.regexp(EDIT_DATE_FROM_PATTERN))
@admin_required
async def handle_edit_client_date_from(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(EDIT_DATE_FROM_PATTERN, callback.data)
    client_id = int(match.group(1))

    current_client = await ClientDAO.find_by_id(client_id)
    if not current_client:
        return await callback.message.answer(client_does_not_exists_error)

    table = await TableDAO.find_one_or_none(id=current_client.table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name
    await state.update_data(client_id=client_id, table_name=table_name)
    await state.set_state(Form.waiting_for_data_new_date_from)

    await callback.message.answer(
        enter_new_date_from_message(table_name=table_name, name=current_client.name)
    )


@router.message(StateFilter(Form.waiting_for_data_new_date_from))
@admin_required
async def handle_client_date_from(message: Message, state: FSMContext):
    new_date_from = message.text.strip()

    if not is_correct_date_part(new_date_from):
        return await message.answer(invalid_date_format_error)

    data = await state.get_data()
    client_id = data.get("client_id")
    current_client = await ClientDAO.find_by_id(client_id)

    if not current_client:
        return await message.answer(client_does_not_exists_error)

    date_to_validate = is_valid_date(
        f"{(parse_date(new_date_from))}.{current_client.date_to}"
    )

    current_date_from = current_client.date_from 

    if not date_to_validate:
        return await message.answer(invalid_date_format_error)

    updated_client = await ClientDAO.update(model_id=client_id, date_from=date_to_validate[0])

    if not updated_client:
        return await message.answer(
            client_date_not_changed_message(current_date=date_to_validate[0])
        )
    await state.clear()
    return await message.answer(
        client_date_changed_successfully_message(
            date=date_to_validate[0], current_date=current_date_from
        ),
        reply_markup=main_keyboard,
    )
