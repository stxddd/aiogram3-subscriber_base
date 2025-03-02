import os
import re

from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from bot.database.clients.dao import ClientDAO
from bot.database.connections.dao import ConnectionDAO
from bot.database.tables.dao import TableDAO
from bot.templates.admin_templates.errors_templates import table_does_not_exist_error
from bot.templates.admin_templates.messages_templates import table_has_no_clients_message
from bot.utils.excel.generate_table import ExcelCRUD

router = Router()

DOWNLOAD_TABLE_PATTERN = r"^download_table_(\d+)$"


@router.callback_query(F.data.regexp(DOWNLOAD_TABLE_PATTERN))
async def handle_download_table(callback: CallbackQuery):
    """Handles downloading the table with its associated data as an Excel file."""
    
    await callback.answer()

    match = re.match(DOWNLOAD_TABLE_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)

    if not table:
        return await callback.message.answer(table_does_not_exist_error)

    table_name = table.name
    tg_id = callback.from_user.id

    clients = await ClientDAO.find_all(table_id=table_id)

    if not clients:
        return await callback.message.answer(
            table_has_no_clients_message(table_name=table_name)
        )

    connections = await ConnectionDAO.find_all()

    file_path = await ExcelCRUD.get_excel_file(
        table_id=table_id, table_name=table_name, tg_id=tg_id, clients=clients, connections=connections
    )

    if not file_path or not file_path.exists():
        return await callback.message.answer(table_does_not_exist_error)

    await callback.message.answer_document(
        document=FSInputFile(file_path),
    )

    os.remove(file_path)
