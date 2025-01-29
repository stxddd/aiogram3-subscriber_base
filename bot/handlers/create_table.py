from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database.tables.dao import TableDAO
from bot.keyboards.home import home_keyboard
from bot.keyboards.utils import cancel_delete_last_keyboard
from bot.templates.errors import (imposible_to_create_table_error,
                                   name_so_long_error
                                  , table_already_exists_error)
from bot.templates.messages import (enter_table_name_message,
                                    table_has_been_created_message,
                                    table_has_been_created_message)
from bot.utils.excel_generator import ExcelCRUD

router = Router()


class Form(StatesGroup):
    waiting_for_table_name = State()
    waiting_for_table_lines = State()


def is_valid_table_name(name: str) -> bool:
    return len(name) <= 32

async def is_not_uniqe_table(name: str, tg_id: int) -> bool:
    return await TableDAO.find_all(name=name, owner_tg_id=tg_id)

async def delete_message_safely(bot, chat_id, message_id):
    try:
        await bot.delete_message(chat_id, message_id)
    except:
        pass  


@router.callback_query(F.data == "create_table")
async def get_table_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    message = await callback.message.answer(enter_table_name_message, reply_markup=cancel_delete_last_keyboard)
    
    await state.update_data(message_sent_id=message.message_id)
    await state.set_state(Form.waiting_for_table_name)

@router.message(StateFilter(Form.waiting_for_table_name))
async def create_table_name(message: Message, state: FSMContext):
    table_name = message.text.strip()

    if not is_valid_table_name(table_name):
        return await message.answer(name_so_long_error)
    
    if await is_not_uniqe_table(table_name, message.from_user.id):
        return await message.answer(table_already_exists_error)

    data = await state.get_data()
    message_sent_id = data.get("message_sent_id")

    await message.bot.delete_message(message.chat.id, message_sent_id)
    try:
        await message.bot.delete_message(message.chat.id, message_sent_id - 1)
    except:
        pass 

    new_table = await TableDAO.add(owner_tg_id=message.from_user.id, name=table_name)
    table = await TableDAO.find_by_id(model_id=new_table["id"])

    if not table:
        return await message.answer(imposible_to_create_table_error, reply_markup=home_keyboard)

    if not await ExcelCRUD.create_new_excel(table_id=table.id, table_name=table.name, tg_id=message.from_user.id):
        await TableDAO.delete(id=table.id)
        return await message.answer(imposible_to_create_table_error, reply_markup=home_keyboard)

    await state.set_state(Form.waiting_for_table_lines)
    await message.answer(table_has_been_created_message(table_name), reply_markup=home_keyboard)