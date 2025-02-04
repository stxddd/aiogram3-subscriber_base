import re
from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.utils.validators import is_valid_price
from bot.keyboards.reply.main_keyboards import main_keyboard
from bot.templates.errors_templates import price_must_be_int_error, client_dose_not_exists_error
from bot.templates.messages_templates import (
    line_price_changed_successfully_message,
    line_price_not_changed_message,
    enter_new_price_message
)
from bot.database.tables.clients.dao import ClientDAO

router = Router()

EDIT_PRICE_PATTERN = r"^edit_data_price_(\d+)_(.+)$"


class Form(StatesGroup):
    waiting_for_data_new_price = State()


@router.callback_query(F.data.regexp(EDIT_PRICE_PATTERN))
async def handle_edit_data_price(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(EDIT_PRICE_PATTERN, callback.data)
    line_id = int(match.group(1))
    table_name = match.group(2)

    current_line = await ClientDAO.find_by_id(line_id)
    if not current_line:
        return await callback.message.answer(client_dose_not_exists_error)

    await state.update_data(line_id=line_id, table_name=table_name)

    await callback.message.answer(
        enter_new_price_message(name=current_line.name, table_name=table_name)
    )
    await state.set_state(Form.waiting_for_data_new_price)


@router.message(StateFilter(Form.waiting_for_data_new_price))
async def handle_new_line_price(message: Message, state: FSMContext):
    if not is_valid_price(message.text.strip()):
        return await message.answer(price_must_be_int_error)

    new_price = int(message.text.strip())

    data = await state.get_data()
    line_id = data.get("line_id")

    current_line = await ClientDAO.find_by_id(line_id)
    if not current_line:
        return await message.answer(client_dose_not_exists_error)

    current_price = current_line.price

    updated_line = await ClientDAO.update(model_id=line_id, price=new_price)
    if updated_line:
        return await message.answer(
            line_price_changed_successfully_message(price=new_price, current_price=current_price),
            reply_markup=main_keyboard
        )

    return await message.answer(line_price_not_changed_message(current_price=current_price))
