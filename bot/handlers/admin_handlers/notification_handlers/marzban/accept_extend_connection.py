from datetime import datetime
import re
from dateutil.relativedelta import relativedelta

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.config import settings
from bot.database.connections.dao import ConnectionDAO
from bot.database.clients.dao import ClientDAO

from bot.keyboards.admin_keyboards.inline.notification_keyboards import extend_connection_keyboard
from bot.templates.admin_templates.messages_templates import (
    client_wants_to_extend_message,
    successful_extension_admin_message,
    successful_extension_message,
)
from bot.templates.user_templates.message_templates import wait_for_admin_message
from bot.utils.marzban.marzban_manager import extend_user
from bot.templates.admin_templates.errors_templates import (
    connection_does_not_exist_error,
    client_does_not_exists_error,
)
from bot.decorators.admin_required import admin_required

router = Router()

ACCEPT_EXTEND_PATTERN = r"^accept_extend_(\d+)_(\d+)_(\d+)$"
EXTEND_PAYMENT_CHECK_COMPLETED = r"extend_payment_check_completed_(\d+)_(\d+)_(\d+)_(\d+)"


@router.callback_query(F.data.regexp(EXTEND_PAYMENT_CHECK_COMPLETED))
async def handle_payment_check_completed(callback: CallbackQuery):
    await callback.answer()
    
    match = re.match(EXTEND_PAYMENT_CHECK_COMPLETED, callback.data)
    connection_id = int(match.group(1))
    new_months = int(match.group(2))
    new_price = int(match.group(3))
    key = int(match.group(4))
    
    connection = await ConnectionDAO.find_by_id(model_id=connection_id)
    if not connection:
        return await callback.message.answer(connection_does_not_exist_error)
    
    client = await ClientDAO.find_one_or_none(id=connection.client_id)
    if not client:
        return await callback.message.answer(client_does_not_exists_error)
    
    date_to_datetime = datetime.combine(connection.date_to, datetime.min.time())
    new_date_to = date_to_datetime + relativedelta(months=new_months)
    
    await callback.message.delete()
    
    await callback.message.bot.send_message(
        client.tg_id,
        wait_for_admin_message
    )
    
    return await callback.message.bot.send_message(
        settings.ADMIN_TG_ID,
        client_wants_to_extend_message(
            username=client.username,
            connection=connection,
            new_date_to=new_date_to,
            old_price=connection.price,
            new_price=new_price,
            key=key,
        ),
        reply_markup=await extend_connection_keyboard(connection_id=connection_id, months=new_months, price=new_price),
    )


@router.callback_query(F.data.regexp(ACCEPT_EXTEND_PATTERN))
@admin_required
async def handle_accept_extend_connection(callback: CallbackQuery):
    await callback.answer()
    
    match = re.match(ACCEPT_EXTEND_PATTERN, callback.data)
    connection_id = int(match.group(1))
    months = int(match.group(2))
    price = int(match.group(3))
    
    connection = await ConnectionDAO.find_one_or_none(id=connection_id)
    
    if not connection:
        return await callback.message.answer(connection_does_not_exist_error)
    
    client = await ClientDAO.find_one_or_none(id=connection.client_id)

    old_date_to = connection.date_to
    old_price = connection.price
    
    date_to_datetime = datetime.combine(connection.date_to, datetime.min.time())
    new_date_to = date_to_datetime + relativedelta(months=months)
    new_price = price
    
    updated_connection = await ConnectionDAO.update(
        model_id=connection.id,
        price=price,
        date_to=new_date_to
    )

    updated_marzban_user = await extend_user(username=connection.name, date_to=new_date_to)
    
    await callback.message.bot.send_message(
        client.tg_id,
        successful_extension_message(
            username=client.username,
            connection=connection,
            new_date_to=new_date_to,
            old_date_to=old_date_to,
            old_price=old_price,
            new_price=new_price,
        )
    )
    
    await callback.message.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    
    await callback.message.bot.send_message(
        settings.ADMIN_TG_ID,
        successful_extension_admin_message(
            connection=connection,
            username=client.username,
            new_date_to=new_date_to,
            old_date_to=old_date_to,
            old_price=old_price,
            new_price=new_price,
        )
    )
