import re

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database.clients.dao import ClientDAO
from bot.keyboards.admin_keyboards.reply.main_keyboards import main_keyboard
from bot.templates.admin_templates.errors_templates import (
    client_does_not_exists_error,
    invalid_date_format_error,
    client_date_not_changed_message,
)
from bot.templates.admin_templates.messages_templates import (
    client_date_changed_successfully_message,
    payment_has_been_completed_message,
)

from bot.utils.data_processing.date_converter import parse_date
from bot.utils.data_processing.validators import is_valid_date, is_correct_date_part
from bot.decorators.admin_required import admin_required

router = Router()

PAYMENT_COMPLETED_PATTERN = r"^payment_completed_(\d+)$"


class Form(StatesGroup):
    waiting_for_new_date_to = State()


@router.callback_query(F.data.regexp(PAYMENT_COMPLETED_PATTERN))
@admin_required
async def handle_payment_completed(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(PAYMENT_COMPLETED_PATTERN, callback.data)
    client_id = int(match.group(1))

    client = await ClientDAO.find_one_or_none(id=client_id)

    if not client:
        return await callback.message.answer(client_does_not_exists_error)

    await callback.message.answer(
        payment_has_been_completed_message(
            client_name=client.username,
            client_date_from=client.date_from,
            client_date_to=client.date_to,
        )
    )
    await state.update_data(client_id=client_id)
    await state.set_state(Form.waiting_for_new_date_to)
    await callback.message.bot.delete_message(
        callback.message.chat.id, callback.message.message_id
    )


@router.message(StateFilter(Form.waiting_for_new_date_to))
@admin_required
async def handle_client_date_to(message: Message, state: FSMContext):
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

    updated_client = await ClientDAO.update(model_id=client_id, date_to=date_to_validate[1], days_late = 0)
    if not updated_client:
        return await message.answer(
            client_date_not_changed_message(current_date=date_to_validate[1])
        )
    
    return await message.answer(
        client_date_changed_successfully_message(
            date=date_to_validate[1], current_date=current_date_to
        ),
        reply_markup=main_keyboard,
    )