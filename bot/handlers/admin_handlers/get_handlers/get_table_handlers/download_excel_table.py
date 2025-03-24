import os
import re

from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from bot.database.clients.dao import ClientDAO
from bot.database.connections.dao import ConnectionDAO
from bot.utils.excel.generate_table import ExcelCRUD
from bot.templates.admin_templates.errors_templates import clients_does_not_exists_error

router = Router()

DOWNLOAD_TABLE_PATTERN = "download_clients"

@router.callback_query(F.data == DOWNLOAD_TABLE_PATTERN)
async def handle_download_table(callback: CallbackQuery):
    await callback.answer()

    clients = await ClientDAO.find_all()
    tg_id = callback.from_user.id

    connections = await ConnectionDAO.find_all()

    file_path = await ExcelCRUD.get_excel_file(
        tg_id=tg_id, clients=clients, connections=connections
    )

    if not file_path or not file_path.exists():
        return await callback.message.answer(clients_does_not_exists_error)

    await callback.message.answer_document(
        document=FSInputFile(file_path),
    )

    os.remove(file_path)
