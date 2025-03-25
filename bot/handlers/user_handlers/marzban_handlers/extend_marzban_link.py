from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.database.clients.dao import ClientDAO
from bot.database.connections.dao import ConnectionDAO
from bot.database.servers.dao import ServerDAO
from bot.handlers.user_handlers.payment_handlers.stars_payment import process_extend_subscription_pay_command
from bot.templates.admin_templates.errors_templates import (
    connection_does_not_exist_error,
    client_does_not_exists_error
)
from bot.keyboards.user_keyboards.inline.marzban_user_info_keyboards import enter_extend_period_keyboard
from bot.templates.user_templates.message_templates import enter_period_message
from bot.templates.user_templates.errors_templates import server_does_not_exists_error

router = Router()

EXTEND_MARZBAN_LINK_PATTERN = r"^extend_marzban_link_(\d+)$"
EXTEND_CONNECTION_DATE_PATTERN = '_connection_period_extend'


@router.callback_query(F.data.regexp(EXTEND_MARZBAN_LINK_PATTERN))
async def handle_extend_marzban_link(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    match = re.match(EXTEND_MARZBAN_LINK_PATTERN, callback.data)
    connection_id = int(match.group(1))
    
    client = await ClientDAO.find_one_or_none(tg_id=callback.from_user.id)
    if client.tg_id != callback.from_user.username:
        client = await ClientDAO.update(model_id=client.id, username=callback.from_user.username)
    
    connection = await ConnectionDAO.find_one_or_none(id=connection_id)
    if not connection:
        return await callback.message.answer(connection_does_not_exist_error)
    
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
        return await callback.message.answer(connection_does_not_exist_error)
    
    date_to_datetime = datetime.combine(connection.date_to, datetime.min.time())
    if date_to_datetime < datetime.today():
        new_date_to = datetime.combine(datetime.today(), datetime.min.time()) + relativedelta(months=int(months)) 
    else:
        new_date_to = date_to_datetime + relativedelta(months=int(months)) 
    new_price = price

    client = await ClientDAO.find_one_or_none(tg_id=callback.from_user.id)
    if not client:
         return await callback.message.answer(client_does_not_exists_error)
    
    server = await ServerDAO.find_by_id(connection.server_id)
    
    if not server:
        return await callback.message.answer(server_does_not_exists_error)
    
    await callback.message.delete()
    
    payload = {"type": 'extend-subscription-payload',
                "connection_id": connection.id,
                "new_date_to": str(new_date_to),
                "new_price": int(new_price)
    }
      
    await process_extend_subscription_pay_command(message = callback.message, price = new_price, payload = payload, os_name=connection.os_name, date_to = new_date_to, server_name = server.name)
    