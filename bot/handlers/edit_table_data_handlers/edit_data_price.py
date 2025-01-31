import re

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.handlers.table_post_handlers.add_data_to_table import is_valid_price
from bot.keyboards.reply.main_keyboards import main_keyboard
from bot.templates.errors_templates import (
    price_must_be_int_error,
)
from bot.templates.messages_templates import (
    line_client_price_changed_successfully_message,
    line_client_price_not_changed_message,
    enter_new_client_price_message
)

from bot.database.tables.lines.dao import LineDAO


router = Router()


class Form(StatesGroup):
    waiting_for_data_new_price = State()


@router.callback_query(F.data.regexp(r"^edit_data_price_(\d+)_(.+)$"))
async def handle_edit_data_price(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    match = re.match(r"^edit_data_price_(\d+)_(.+)$", callback.data)

    line_id = int(match.group(1))
    table_name = match.group(2)

    current_line = await LineDAO.find_by_id(line_id)

    old_client_name = current_line.subscriber_tg_id

    await state.update_data(line_id=line_id, table_name=table_name)
    await callback.message.answer(enter_new_client_price_message(client_name=old_client_name, table_name=table_name))
    await state.set_state(Form.waiting_for_data_new_price)


@router.message(StateFilter(Form.waiting_for_data_new_price))
async def handle_new_line_price(message: Message, state: FSMContext):
    if not is_valid_price(message.text.strip()):
        return await message.answer(price_must_be_int_error)

    new_client_price = int(message.text.strip())

    data = await state.get_data()
    table_name = data.get("table_name")
    line_id = data.get("line_id")

    current_line = await LineDAO.find_by_id(line_id)

    old_client_price = current_line.subscriber_price
    if current_line:
        updated_line = await LineDAO.update(model_id=line_id, subscriber_price=new_client_price)
        return await message.answer(line_client_price_changed_successfully_message(client_price=new_client_price, old_client_price=old_client_price), reply_markup = main_keyboard)

    return message.answer(line_client_price_not_changed_message(old_client_price=old_client_price))