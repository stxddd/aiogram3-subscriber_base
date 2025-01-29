import re

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database.tables.lines.dao import LineDAO
from bot.keyboards.home import home_keyboard
from bot.keyboards.utils import back_keyboard
from bot.templates.errors import (adding_data_error, 
                                  name_so_long_error, 
                                  price_must_be_int_error,
                                  invalid_date_format_error)
from bot.templates.messages import (main_menu, data_added_message,
                                     sent_client_name_message,
                                       sent_client_price_message, 
                                       sent_client_date_message)
from bot.utils.excel_generator import ExcelCRUD

router = Router()


class Form(StatesGroup):
    waiting_for_name_data = State()
    waiting_for_price_data = State()
    waiting_for_date_data = State()


def is_valid_date(date: str) -> bool:
    return bool(re.fullmatch(r"\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}", date))

def is_valid_price(price: str) -> bool:
    return price.isdigit()

def is_valid_name(name: str) -> bool:
    return len(name) <= 32

async def delete_message_safely(bot, chat_id, message_id):
    try:
        await bot.delete_message(chat_id, message_id)
    except:
        pass  

@router.callback_query(F.data == "add_data_to_table")
async def add_line_to_table(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await delete_message_safely(callback.message.bot, callback.message.chat.id, data.get("message_sent_id_actions_with_table"))

    message_sent = await callback.message.answer(sent_client_name_message, reply_markup=back_keyboard)
    await state.update_data(message_sent_id_name=message_sent.message_id)
    
    await callback.answer()
    await state.set_state(Form.waiting_for_name_data)

@router.message(StateFilter(Form.waiting_for_name_data))
async def get_name(message: Message, state: FSMContext):
    name = message.text.strip()

    if not is_valid_name(name):
        return await message.answer(name_so_long_error)

    data = await state.get_data()
    await delete_message_safely(message.bot, message.chat.id, data.get("message_sent_id_name"))

    message_sent = await message.answer(sent_client_price_message, reply_markup=back_keyboard)
    await state.update_data(name=name, message_sent_id_price=message_sent.message_id)
    
    await state.set_state(Form.waiting_for_price_data)

@router.message(StateFilter(Form.waiting_for_price_data))
async def get_price(message: Message, state: FSMContext):
    price = message.text.strip()

    if not is_valid_price(price):
        return await message.answer(price_must_be_int_error)

    data = await state.get_data()
    await delete_message_safely(message.bot, message.chat.id, data.get("message_sent_id_price"))

    message_sent = await message.answer(sent_client_date_message, reply_markup=back_keyboard)

    await state.update_data(price=int(price), message_sent_id_date=message_sent.message_id)
    await state.set_state(Form.waiting_for_date_data)

@router.message(StateFilter(Form.waiting_for_date_data))
async def get_date(message: Message, state: FSMContext):
    date = message.text.strip()

    if not is_valid_date(date):
        return await message.answer(invalid_date_format_error)

    data = await state.get_data()
    name, price, table_id, table_name = data.get("name"), data.get("price"), data.get("table_id"), data.get("table_name")

    new_line = await LineDAO.add(
        owner_tg_id=message.from_user.id, table_id=table_id, subscriber_tg_id=name, subscriber_price=price, subscriber_date=date
    )

    if not new_line:
        return await message.answer(adding_data_error)

    if not await ExcelCRUD.add_words_to_existing_excel(data=[name, price, date], table_id=table_id, tg_id=message.from_user.id, table_name=table_name):
        await LineDAO.delete(owner_tg_id=message.from_user.id, table_id=table_id, subscriber_tg_id=name, subscriber_price=price, subscriber_date=date)
        return await message.answer(adding_data_error)

    success_message = await message.answer(data_added_message(table_name, name, price, date ))

    await delete_message_safely(message.bot, message.chat.id, data.get("message_sent_id_date"))
    
    await state.update_data(date=date, message_ids=[success_message.message_id])
    await message.answer(main_menu, reply_markup=home_keyboard)
    await state.clear()