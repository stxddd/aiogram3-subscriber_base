from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.database.tables.dao import TableDAO
from bot.database.users.dao import UserDAO
from bot.keyboards.admin_keyboards.inline.table_keyboards import get_actions_with_table_keyboard
from bot.keyboards.admin_keyboards.inline.utils_keyboards import cancel_delete_last_keyboard

from bot.templates.admin_templates.errors_templates import (
    imposible_to_create_table_error,
    name_so_long_error,
    table_already_exists_error,
)
from bot.templates.admin_templates.keyboards_templates import create_table_text
from bot.templates.admin_templates.messages_templates import (
    enter_table_name_message,
    table_has_been_created_message,
)
from bot.templates.user_templates.errors_templates import (
    auth_error,
)
from bot.utils.data_processing.validators import is_valid_name
from bot.decorators.admin_required import admin_required

router = Router()


class Form(StatesGroup):
    waiting_for_table_name = State()


async def is_not_uniqe_table(name: str, user_id: int) -> bool:
    return await TableDAO.find_all(name=name, user_id=user_id)


@router.message(F.text == create_table_text)
@admin_required
async def handle_create_table(message: Message, state: FSMContext):
    """Ловит команду на создание Базы, уточняет ее имя."""
    
    user = await UserDAO.find_one_or_none(tg_id = message.from_user.id)
    
    if not user:
        return await message.answer(auth_error)

    await state.set_state(Form.waiting_for_table_name)
    return await message.answer(
        enter_table_name_message, reply_markup=cancel_delete_last_keyboard
    )



@router.message(StateFilter(Form.waiting_for_table_name))
@admin_required
async def handle_table_name(message: Message, state: FSMContext):
    "Ловит имя и создает базу"
    
    table_name = message.text.strip()
    user = await UserDAO.find_one_or_none(tg_id = message.from_user.id)

    if not user:
        return await message.answer(auth_error)
    
    if not is_valid_name(table_name):
        return await message.answer(name_so_long_error)

    if await is_not_uniqe_table(table_name,user.id):
        return await message.answer(table_already_exists_error)

    new_table = await TableDAO.add(user_id=user.id, name=table_name)
    table = await TableDAO.find_by_id(model_id=new_table["id"])

    if not table:
        return await message.answer(imposible_to_create_table_error)

    await state.clear()

    return await message.answer(
        table_has_been_created_message(table_name),
        reply_markup=await get_actions_with_table_keyboard(table_id=table.id),
    )
