from datetime import datetime
from dateutil.relativedelta import relativedelta
from random import randint

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.config import settings
from bot.database.connections.dao import ConnectionDAO
from bot.database.clients.dao import ClientDAO
from bot.database.users.dao import UserDAO
from bot.keyboards.user_keyboards.inline.payment_keyboards import get_check_pay_connect_keyboard
from bot.templates.user_templates.message_templates import marzban_day_limit_message, wait_for_payment_message
from bot.templates.user_templates.errors_templates import added_connection_error
from bot.templates.user_templates.keyboards_templates import get_new_connection_text
from bot.keyboards.user_keyboards.inline.marzban_user_info_keyboards import enter_os_keyboard,enter_period_keyboard
from bot.templates.user_templates.message_templates import enter_os_message, enter_period_message

router = Router()

ADD_CONNECTION_DATE_PATTERN = '_connection_period'
ADD_CONNECTION_OS_PATTERN = '_add_connection_os'


@router.message(F.text == get_new_connection_text)
async def handle_new_connection_selection(message: Message):
    "Ловит команду на добавление нового подключения, отправляет сообщение с выбором периода"
    
    user = await UserDAO.find_one_or_none(tg_id = message.from_user.id)
    if user.marzban_requests_today > settings.MARZBAN_REQUEST_DAY_LIMIT:
        return await message.answer(marzban_day_limit_message)
    
    return await message.answer(enter_period_message, reply_markup=enter_period_keyboard)


@router.callback_query(lambda c: c.data.endswith(ADD_CONNECTION_DATE_PATTERN))
async def handle_period_selection(callback: CallbackQuery, state: FSMContext):
    "Ловит выбор периода, сохраняет в state, отправляет сообщение с выбором ОС"
    
    await callback.answer()
    months = callback.data.split("_")[0]
    price = callback.data.split("_")[1]
    await state.update_data(months = months, price = price)
    await callback.message.delete()
    return await callback.message.answer(enter_os_message, reply_markup=enter_os_keyboard)


@router.callback_query(lambda c: c.data.endswith(ADD_CONNECTION_OS_PATTERN))
async def handle_add_new_connection(callback: CallbackQuery, state: FSMContext):
    "Ловит выбор ОС, сохраняет в state, отправляет запрос на оплату"
    
    await callback.answer()
    
    tg_id = callback.from_user.id

    user = await UserDAO.find_one_or_none(tg_id = tg_id)

    if user.marzban_requests_today > settings.MARZBAN_REQUEST_DAY_LIMIT:
        return await callback.message.answer(marzban_day_limit_message)
    
    data = await state.get_data()
    date_to = datetime.now() + relativedelta(months=int(data.get('months')), days=1)
    price = int(data.get('price'))
        
    marzban_requests_today = user.marzban_requests_today + 1 

    updated_user = await UserDAO.update(
        model_id=user.id, 
        marzban_requests_today = marzban_requests_today,
        last_marzban_request_date = datetime.now()
    )

    client = await ClientDAO.find_one_or_none(tg_id = tg_id)
    
    if not client:
        new_client = await ClientDAO.add(
            username = callback.from_user.username if callback.from_user.username else '-',
            tg_id = tg_id
        )
        if not new_client:
            return await callback.message.answer(added_connection_error)
        client = await ClientDAO.find_one_or_none(tg_id = tg_id)
        
    user_os = callback.data.split("_")[0]  
    username = callback.from_user.username or callback.from_user.id

    connection_name = f"{user_os}_{username}_{randint(10000,99999)}"
    
    added_connection = await ConnectionDAO.add(
        client_id = client.id,
        date_to = date_to,
        price = price,
        os_name = user_os,
        name = connection_name
    )    
    
    connection = await ConnectionDAO.find_by_id(added_connection.id)
    
    await callback.message.delete()
    
    key = randint(1000,9999)
    
    await callback.message.answer(
        wait_for_payment_message(connection = connection, price = price, key = key),
        reply_markup= await get_check_pay_connect_keyboard(connection_id = connection.id, key = key)    
    )
