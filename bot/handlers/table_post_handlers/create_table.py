from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.database.tables.dao import TableDAO
from bot.keyboards.inline.table_keyboards import get_actions_with_table_keyboard
from bot.keyboards.inline.utils_keyboards import cancel_delete_last_keyboard
from bot.templates.errors_templates import (imposible_to_create_table_error,
                                   name_so_long_error
                                  , table_already_exists_error)
from bot.templates.messages_templates import (enter_table_name_message,
                                    table_has_been_created_message,
                                    table_has_been_created_message)
from bot.templates.keyboards_templates import create_table_text

router = Router()


class Form(StatesGroup):
    waiting_for_table_name = State()


def is_valid_table_name(name: str) -> bool:
    return len(name) <= 32

async def is_not_uniqe_table(name: str, tg_id: int) -> bool:
    return await TableDAO.find_all(name=name, owner_tg_id=tg_id)


@router.message(F.text == create_table_text)
async def handle_create_table(message: Message, state: FSMContext):
    message = await message.answer(enter_table_name_message, reply_markup=cancel_delete_last_keyboard)

    await state.set_state(Form.waiting_for_table_name)


@router.message(StateFilter(Form.waiting_for_table_name))
async def handle_table_name(message: Message, state: FSMContext):
    table_name = message.text.strip()

    if not is_valid_table_name(table_name):
        return await message.answer(name_so_long_error)
    
    if await is_not_uniqe_table(table_name, message.from_user.id):
        return await message.answer(table_already_exists_error)

    new_table = await TableDAO.add(owner_tg_id=message.from_user.id, name=table_name)
    table = await TableDAO.find_by_id(model_id=new_table["id"])

    if not table:
        return await message.answer(imposible_to_create_table_error)

    await message.answer(table_has_been_created_message(table_name), reply_markup = await get_actions_with_table_keyboard(table.id, table.name))