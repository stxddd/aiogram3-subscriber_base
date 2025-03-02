from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
from random import randint

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.clients.dao import ClientDAO
from bot.database.connections.dao import ConnectionDAO
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.keyboards.user_keyboards.inline.payment_keyboards import get_check_pay_keyboard
from bot.templates.admin_templates.errors_templates import (
    connection_dose_not_exists_error,
    client_does_not_exists_error
)
from bot.keyboards.user_keyboards.inline.marzban_user_info_keyboards import enter_extend_period_keyboard
from bot.templates.user_templates.message_templates import enter_period_message, wait_for_payment_message

router = Router()

EXTEND_MARZBAN_LINK_PATTERN = r"^extend_marzban_link_(\d+)$"
EXTEND_CONNECTION_DATE_PATTERN = '_connection_period_extend'


@router.callback_query(F.data.regexp(EXTEND_MARZBAN_LINK_PATTERN))
async def handle_extend_marzban_link(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    match = re.match(EXTEND_MARZBAN_LINK_PATTERN, callback.data)
    connection_id = int(match.group(1))
    
    connection = await ConnectionDAO.find_one_or_none(id=connection_id)
    if not connection:
        return await callback.message.answer(connection_dose_not_exists_error)
    
    await state.update_data(connection_id=connection.id)
   
    return await callback.message.answer(enter_period_message, reply_markup=enter_extend_period_keyboard)


@router.callback_query(lambda c: c.data.endswith(EXTEND_CONNECTION_DATE_PATTERN))
async def handle_period_selection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    months = callback.data.split("_")[0]
    price = callback.data.split("_")[1]
    
    data = await state.get_data()
    
    connection_id = data.get('connection_id')
    connection = await ConnectionDAO.find_one_or_none(id=connection_id)
    
    if not connection:
        return await callback.message.answer(connection_dose_not_exists_error)
    
    date_to_datetime = datetime.combine(connection.date_to, datetime.min.time())
    new_date_to = date_to_datetime + relativedelta(months=int(months))

    old_price = connection.price
    new_price = price

    client = await ClientDAO.find_one_or_none(tg_id = callback.from_user.id)
    if not client:
         return await callback.message.answer(client_does_not_exists_error)
    
    
    await callback.message.delete()
    
    key = randint(1000,9999)
    
    await callback.message.answer(
        wait_for_payment_message(connection = connection, price = price, key = key),
        reply_markup= await get_check_pay_keyboard(connection_id = connection.id, new_price = new_price, new_months = months, key = key)    
    )
