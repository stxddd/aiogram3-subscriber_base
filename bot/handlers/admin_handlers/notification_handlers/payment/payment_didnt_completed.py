import re
from datetime import timedelta

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.clients.dao import ClientDAO
from bot.templates.admin_templates.errors_templates import client_does_not_exists_error
from bot.templates.admin_templates.messages_templates import payment_didnt_completed_message

router = Router()

PAYMENT_DIDNT_COMPLETED_PATTERN = r"^payment_didnt_completed_(\d+)$"


@router.callback_query(F.data.regexp(PAYMENT_DIDNT_COMPLETED_PATTERN))
async def handle_payment_didnt_completed(callback: CallbackQuery):
    await callback.answer()

    match = re.match(PAYMENT_DIDNT_COMPLETED_PATTERN, callback.data)
    client_id = int(match.group(1))

    client = await ClientDAO.find_one_or_none(id=client_id)

    if not client:
        return await callback.message.answer(client_does_not_exists_error)

    days_late = client.days_late

    if not days_late:
        days_late = 1
    else:
        days_late += 1

    client = await ClientDAO.update(model_id=client.id, days_late=days_late)

    if not client:
        return await callback.message.answer(client_does_not_exists_error)

    await callback.message.answer(
        payment_didnt_completed_message(client_name=client.username, days_late=days_late)
    )
    await callback.message.bot.delete_message(
        callback.message.chat.id, callback.message.message_id
    )
