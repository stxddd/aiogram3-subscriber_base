import re

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.handlers.table_post_handlers.add_data_to_table import is_valid_name
from bot.keyboards.reply.main_keyboards import main_keyboard
from bot.templates.errors_templates import (
    name_so_long_error,line_dose_not_exists_error
)
from bot.templates.messages_templates import (
    line_client_name_changed_successfully_message,
    line_client_name_not_changed_message,
    enter_new_client_name_message
)

from bot.database.tables.lines.dao import LineDAO

router = Router()


class Form(StatesGroup):
    waiting_for_data_new_name = State()


@router.callback_query(F.data.regexp(r"^edit_data_name_(\d+)_(.+)$"))
async def handle_edit_data_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    match = re.match(r"^edit_data_name_(\d+)_(.+)$", callback.data)

    line_id = int(match.group(1))
    table_name = match.group(2)

    current_line = await LineDAO.find_one_or_none(id=line_id)
    
    if not current_line:
        return await callback.message.answer(line_dose_not_exists_error)

    old_client_name = current_line.subscriber_tg_id

    await state.update_data(line_id=line_id, table_name=table_name)
    await callback.message.answer(enter_new_client_name_message(table_name=table_name, client_name=old_client_name))
    await state.set_state(Form.waiting_for_data_new_name)


@router.message(StateFilter(Form.waiting_for_data_new_name))
async def handle_new_line_name(message: Message, state: FSMContext):
    new_client_name = message.text.strip()

    if not is_valid_name(new_client_name):
        return await message.answer(name_so_long_error)

    data = await state.get_data()
    line_id = data.get("line_id")

    current_line = await LineDAO.find_by_id(line_id)
    
    old_client_name = current_line.subscriber_tg_id

    if current_line:
        updated_line = await LineDAO.update(model_id=line_id, subscriber_tg_id=new_client_name)
        return await message.answer(line_client_name_changed_successfully_message(client_name=new_client_name, old_client_name=old_client_name), reply_markup = main_keyboard)

    return message.answer(line_client_name_not_changed_message(old_client_name=old_client_name))