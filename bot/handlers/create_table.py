from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database.tables.dao import TableDAO
from bot.keyboards.home import delete_last_keyboard
from bot.templates.errors import imposible_to_create_table_error
from bot.templates.messages import (enter_table_name_message,
                                    table_has_been_created_message)
from bot.utils.excel_generator import ExcelCRUD
from bot.keyboards.tables import get_my_tables_keyboard

router = Router()


class Form(StatesGroup):
    waiting_for_table_name = State()
    waiting_for_table_lines = State()


@router.callback_query(F.data == "create_table")
async def get_table_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    message_sent = await callback.message.answer(
        enter_table_name_message, reply_markup=delete_last_keyboard
    )
    
    await state.update_data(message_sent_id=message_sent.message_id)
    await state.set_state(Form.waiting_for_table_name)


@router.message(StateFilter(Form.waiting_for_table_name))
async def create_table_name(message: Message, state: FSMContext):
    data = await state.get_data()
    message_sent_id = data.get("message_sent_id")
    await message.bot.delete_message(message.chat.id, message_sent_id)

    new_table = await TableDAO.add(owner_tg_id=message.from_user.id, name=message.text)
    table = await TableDAO.find_by_id(model_id=new_table["id"])
    new_exel_table = await ExcelCRUD.create_new_excel(
        table_id=table.id, table_name=table.name, tg_id=message.from_user.id
    )

    if not table:
        return await message.answer(imposible_to_create_table_error)

    await state.set_state(Form.waiting_for_table_lines)
    return await message.answer(table_has_been_created_message + table.name)