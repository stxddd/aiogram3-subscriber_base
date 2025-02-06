import re

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.tables.clients.dao import ClientDAO
from bot.database.tables.dao import TableDAO
from bot.templates.errors_templates import (
    clients_does_not_exists_error,
    table_dose_not_exists_error,
)
from bot.templates.messages_templates import table_base_info_message

router = Router()

GET_STATISTIC_PATTERN = r"^get_table_info_(\d+)$"


@router.callback_query(F.data.regexp(GET_STATISTIC_PATTERN))
async def handle_base_table_info(callback: CallbackQuery):
    await callback.answer()

    match = re.match(GET_STATISTIC_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    clients = await ClientDAO.find_all(table_id=table_id)

    if not clients:
        return await callback.message.answer(clients_does_not_exists_error)

    clients_count = len(clients)

    all_prices = await ClientDAO.count_all_prices(table_id=table_id)

    if not all_prices:
        return await callback.message.answer(clients_does_not_exists_error)

    await callback.message.answer(
        table_base_info_message(
            table_name=table_name, clients_count=clients_count, all_prices=all_prices
        )
    )
