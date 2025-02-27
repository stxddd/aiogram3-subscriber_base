import re

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.connections.dao import ConnectionDAO
from bot.database.clients.dao import ClientDAO
from bot.database.tables.dao import TableDAO
from bot.keyboards.admin_keyboards.inline.clients_keyboards import (
    get_clients_data_unit_to_edit,
    get_clients_for_edit,
)
from bot.keyboards.admin_keyboards.inline.connections_keyboards import get_connections_to_edit
from bot.templates.admin_templates.errors_templates import (
    connection_dose_not_exists_error
)
from bot.templates.admin_templates.messages_templates import (
    one_client_message,
    table_base_info_message,
    table_has_no_clients_message,
)
from bot.decorators.admin_required import admin_required
from bot.keyboards.user_keyboards.inline.marzban_user_info_keyboards import enter_period_keyboard
from bot.templates.user_templates.message_templates import enter_period_message

router = Router()


EXTEND_MARZBAN_LINK_PATTERN = r"^extend_marzban_link_(\d+)$"


@router.callback_query(F.data.regexp(EXTEND_MARZBAN_LINK_PATTERN))
@admin_required
async def handle_extend_marzban_link(callback: CallbackQuery):
    await callback.answer()
    
    match = re.match(EXTEND_MARZBAN_LINK_PATTERN, callback.data)
    connection_id = int(match.group(1))
    
    connection = await ConnectionDAO.find_one_or_none(id=connection_id)
    if not connection:
        return await callback.message.answer(connection_dose_not_exists_error)
    
    return await callback.message.answer(enter_period_message, reply_markup=enter_period_keyboard)

@router.callback_query(lambda c: c.data.endswith(ADD_CONNECTION_DATE_PATTERN))
async def handle_period_selection(callback: CallbackQuery, state: FSMContext):
    "Ловит выбор периода, сохраняет в state, отправляет сообщение с выбором ОС"
    
    await callback.answer()
    months = callback.data.split("_")[0]
    price = callback.data.split("_")[1]
    await state.update_data(months = months, price = price)
    await callback.message.delete()
    