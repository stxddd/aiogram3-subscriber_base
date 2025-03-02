import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from bot.database.tables.dao import TableDAO
from bot.keyboards.admin_keyboards.inline.utils_keyboards import (
    yes_or_not_delte_table_keyboard, cancel_delete_last_keyboard
)
from bot.templates.admin_templates.errors_templates import table_does_not_exist_error
from bot.templates.admin_templates.messages_templates import (
    are_you_sure_to_delete_table_message,
    enter_code_for_delete_table,
    table_are_deleted_message,
    table_are_not_deleted_message,
    incorrect_code_message,
)
from bot.decorators.admin_required import admin_required
from bot.config import settings

router = Router()


class Form(StatesGroup):
    enter_secret_code_for_delete_table = State()


PREPARE_TO_DELTE_TABLE_PATTERN = r"^prepare_to_delete_table_(\d+)$"
DELETE_TABLE_PATTERN = r"^delete_table_(\d+)$"


@router.callback_query(F.data.regexp(PREPARE_TO_DELTE_TABLE_PATTERN))
@admin_required
async def handle_prepare_to_delete_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(PREPARE_TO_DELTE_TABLE_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)

    if not table:
        return await callback.message.answer(table_does_not_exist_error)

    table_name = table.name

    await callback.message.answer(
        are_you_sure_to_delete_table_message(table_name),
        reply_markup=await yes_or_not_delte_table_keyboard(table_id=table_id),
    )


@router.callback_query(F.data.regexp(DELETE_TABLE_PATTERN))
@admin_required
async def handle_delete_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(DELETE_TABLE_PATTERN, callback.data)
    table_id = int(match.group(1))

    await state.update_data(table_id=table_id)

    table = await TableDAO.find_one_or_none(id=table_id)

    if not table:
        return await callback.message.answer(table_does_not_exist_error)

    table_name = table.name

    await state.set_state(Form.enter_secret_code_for_delete_table)
    return await callback.message.answer(
        enter_code_for_delete_table(table_name=table_name),
        reply_markup=cancel_delete_last_keyboard,
    )


@router.message(StateFilter(Form.enter_secret_code_for_delete_table))
async def handle_delete_secret_key(message: Message, state: FSMContext):
    code = message.text

    if code != settings.KEY_FOR_DELETE:
        await message.answer(incorrect_code_message)
    else:
        data = await state.get_data()
        table_id = data.get("table_id")

        table = await TableDAO.find_one_or_none(id=table_id)
        table_name = table.name

        delete_table = await TableDAO.delete(id=table_id)

        if not delete_table:
            await message.answer(table_are_not_deleted_message(table_name))

        await message.answer(table_are_deleted_message(table_name))
