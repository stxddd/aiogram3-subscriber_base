import re

from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.config import settings
from bot.database.tables.clients.dao import ClientDAO
from bot.database.tables.dao import TableDAO
from bot.keyboards.inline.table_keyboards import \
    get_actions_with_table_keyboard
from bot.keyboards.inline.utils_keyboards import cancel_delete_last_keyboard
from bot.keyboards.reply import main_keyboards
from bot.templates.errors_templates import (
    adding_data_error, exceeded_the_limit_on_the_line_error,
    invalid_date_format_error, name_so_long_error, price_must_be_int_error,
    table_dose_not_exists_error)
from bot.templates.messages_templates import (data_added_message,
                                              sent_date_message,
                                              sent_name_message,
                                              sent_price_message)
from bot.utils.data_processing.date_converter import get_date_for_db
from bot.utils.data_processing.validators import (is_valid_date, is_valid_name,
                                                  is_valid_price)

router = Router()


class Form(StatesGroup):
    waiting_for_name_data = State()
    waiting_for_price_data = State()
    waiting_for_date_data = State()


async def delete_message_safely(bot, chat_id, message_id):
    try:
        await bot.delete_message(chat_id, message_id)
    except:
        pass


ADD_DATA_PATTERN = r"^add_data_to_table_(\d+)$"


@router.callback_query(F.data.regexp(ADD_DATA_PATTERN))
async def handle_add_line_to_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(ADD_DATA_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    clients = await ClientDAO.find_all(table_id=table_id)

    if len(clients) <= settings.MAX_CLIENT_LIMIT:
        message_sent = await callback.message.answer(
            sent_name_message(table_name), reply_markup=cancel_delete_last_keyboard
        )
        await state.update_data(
            table_id=table_id,
            table_name=table_name,
            message_sent_id_name=message_sent.message_id,
        )
        return await state.set_state(Form.waiting_for_name_data)

    return await callback.message.answer(
        exceeded_the_limit_on_the_line_error, reply_markup=main_keyboards
    )


@router.message(StateFilter(Form.waiting_for_name_data))
async def handle_client_name(message: Message, state: FSMContext):
    name = message.text.strip()

    data = await state.get_data()
    table_name = data.get("table_name")

    if not is_valid_name(name):
        return await message.answer(name_so_long_error)

    await delete_message_safely(
        message.bot, message.chat.id, data.get("message_sent_id_name")
    )

    message_sent = await message.answer(
        sent_price_message(table_name), reply_markup=cancel_delete_last_keyboard
    )

    await state.update_data(name=name, message_sent_id_price=message_sent.message_id)
    await state.set_state(Form.waiting_for_price_data)


@router.message(StateFilter(Form.waiting_for_price_data))
async def handle_client_price(message: Message, state: FSMContext):
    price = message.text.strip()

    if not is_valid_price(price):
        return await message.answer(price_must_be_int_error)

    data = await state.get_data()
    table_name = data.get("table_name")

    await delete_message_safely(
        message.bot, message.chat.id, data.get("message_sent_id_price")
    )

    message_sent = await message.answer(
        sent_date_message(table_name), reply_markup=cancel_delete_last_keyboard
    )

    await state.update_data(
        price=int(price), message_sent_id_date=message_sent.message_id
    )
    await state.set_state(Form.waiting_for_date_data)


@router.message(StateFilter(Form.waiting_for_date_data))
async def handle_client_date(message: Message, state: FSMContext):
    date = message.text.strip()

    if not is_valid_date(date):
        return await message.answer(invalid_date_format_error)

    date = get_date_for_db(date).split("-")

    data = await state.get_data()
    name, price, table_id, table_name = (
        data.get("name"),
        data.get("price"),
        data.get("table_id"),
        data.get("table_name"),
    )

    new_client = await ClientDAO.add(
        table_id=table_id,
        name=name,
        price=price,
        date_from=date[0],
        date_to=date[1],
    )

    if not new_client:
        return await message.answer(adding_data_error)

    await delete_message_safely(
        message.bot, message.chat.id, data.get("message_sent_id_date")
    )
    await message.answer(
        data_added_message(table_name, name, price, date),
        reply_markup=await get_actions_with_table_keyboard(table_id),
    )
