import re

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database.tables.dao import TableDAO
from bot.keyboards.admin_keyboards.inline.utils_keyboards import cancel_delete_last_keyboard
from bot.keyboards.admin_keyboards.reply.main_keyboards import main_keyboard
from bot.templates.admin_templates.errors_templates import (
    name_so_long_error,
    table_dose_not_exists_error,
    table_name_not_changed_error,
)
from bot.templates.admin_templates.messages_templates import (
    enter_new_table_name_message,
    table_name_changed_successfully_message,
)
from bot.utils.data_processing.validators import is_valid_name
from bot.decorators.admin_required import admin_required

router = Router()


class Form(StatesGroup):
    waiting_for_new_table_name_data = State()


EDIT_TABLE_NAME_PATTERN = r"^edit_name_(\d+)$"


@router.callback_query(F.data.regexp(EDIT_TABLE_NAME_PATTERN))
@admin_required
async def handle_edit_table_name(callback: CallbackQuery, state: FSMContext):
    """Ловит команду на изменение имени таблицы, уточняет новое имя."""
    await callback.answer()

    match = re.match(EDIT_TABLE_NAME_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    message_sent = await callback.message.answer(
        enter_new_table_name_message(table_name),
        reply_markup=cancel_delete_last_keyboard,
    )

    await state.update_data(
        table_id=table_id,
        table_name=table_name,
        message_sent_id_name=message_sent.message_id,
    )
    await state.set_state(Form.waiting_for_new_table_name_data)


@router.message(StateFilter(Form.waiting_for_new_table_name_data))
@admin_required
async def handle_table_name(message: Message, state: FSMContext):
    """Переименовывает таблицу"""
    new_table_name = message.text.strip()

    if not is_valid_name(new_table_name):
        return await message.answer(name_so_long_error)

    data = await state.get_data()
    table_name = data.get("table_name")
    table_id = data.get("table_id")

    current_table = await TableDAO.find_by_id(table_id)

    if not current_table:
        return message.answer(table_name_not_changed_error(table_name=table_name))
    
    updated_table = await TableDAO.update(model_id=table_id, name=new_table_name)
    if not updated_table:
        return message.answer(table_name_not_changed_error(table_name=table_name))
    
    await state.clear()
    return await message.answer(
        table_name_changed_successfully_message(
            table_name=new_table_name, current_table_name=table_name
        ),
        reply_markup=main_keyboard,
    )

   
