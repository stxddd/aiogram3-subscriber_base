import re

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database.tables.clients.dao import ClientDAO
from bot.keyboards.reply.main_keyboards import main_keyboard
from bot.templates.errors_templates import (
    client_dose_not_exists_error,
    invalid_date_format_error,
)
from bot.templates.messages_templates import (
    line_date_changed_successfully_message,
    line_date_not_changed_message,
    payment_has_been_completed_message,
)
from bot.utils.data_processing.date_converter import (
    convert_to_short_format,
    get_date_for_db,
)
from bot.utils.data_processing.validators import is_valid_date, is_valid_date_part

router = Router()

PAYMENT_COMPLETED_PATTERN = r"^payment_completed_(\d+)$"


class Form(StatesGroup):
    waiting_for_new_date_to = State()


@router.callback_query(F.data.regexp(PAYMENT_COMPLETED_PATTERN))
async def handle_base_table_info(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(PAYMENT_COMPLETED_PATTERN, callback.data)
    client_id = int(match.group(1))

    client = await ClientDAO.find_one_or_none(id=client_id)

    if not client:
        return await callback.message.answer(client_dose_not_exists_error)

    await callback.message.answer(
        payment_has_been_completed_message(
            client_name=client.name,
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
async def handle_line_date_to(message: Message, state: FSMContext):
    new_date_to = message.text.strip()

    if not is_valid_date_part(new_date_to):
        return await message.answer(invalid_date_format_error)

    new_date_to = get_date_for_db(new_date_to)

    data = await state.get_data()
    client_id = data.get("client_id")

    current_client = await ClientDAO.find_by_id(client_id)
    if not current_client:
        return await message.answer(client_dose_not_exists_error)

    current_date_to = current_client.date_to

    date_to_validate = convert_to_short_format(
        f"{current_client.date_from}-{new_date_to}"
    )

    if not date_to_validate or not is_valid_date(date_to_validate):
        return await message.answer(
            line_date_not_changed_message(current_date=current_date_to)
        )

    updated_client = await ClientDAO.update(
        model_id=client_id, date_to=new_date_to, days_late=0
    )
    if updated_client:
        return await message.answer(
            line_date_changed_successfully_message(
                date=new_date_to, current_date=current_date_to
            ),
            reply_markup=main_keyboard,
        )

    return await message.answer(
        line_date_not_changed_message(current_date=current_date_to)
    )
