from datetime import datetime
import os
from pathlib import Path
import re

from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from bot.database.tables.clients.dao import ClientDAO
from bot.database.tables.dao import TableDAO
from bot.database.users.dao import UserDAO
from bot.keyboards.inline.table_keyboards import get_actions_with_table_keyboard
from bot.templates.errors_templates import table_dose_not_exists_error, excel_table_can_not_create_error, exceeded_the_limit_on_the_table_download_error
from bot.templates.messages_templates import table_has_no_lines_message
from bot.utils.excel.excel_generator import ExcelCRUD
from bot.config import settings

router = Router()

DOWNLOAD_TABLE_PATTERN = r"^download_table_(\d+)$"

@router.callback_query(F.data.regexp(DOWNLOAD_TABLE_PATTERN))
async def handle_download_table(callback: CallbackQuery):
    await callback.answer()

    match = re.match(DOWNLOAD_TABLE_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)
    
    table_name = table.name
    tg_id = callback.from_user.id

    table = await TableDAO.find_one_or_none(id=table_id)

    clients = await ClientDAO.find_all(table_id=table_id)

    if not clients:
        return await callback.message.answer(table_has_no_lines_message(table_name=table_name))

    user = await UserDAO.find_one_or_none(tg_id=tg_id)
    user.reset_if_new_day()

    if user.downloads_today >= settings.DOWNLOAD_DAY_LIMIT:
        return await callback.message.answer(exceeded_the_limit_on_the_table_download_error)

    downloads_today = user.downloads_today 
    await UserDAO.update(model_id=user.id, downloads_today= downloads_today + 1, last_download_date = datetime.now() )
    
    excel_file = await ExcelCRUD.get_excel_file(
        table_id=table_id, 
        table_name=table_name, 
        tg_id=tg_id, 
        clients=clients)
    
    if not excel_file:
        return await callback.message.answer(excel_table_can_not_create_error(table_name=table_name))

    file_path = Path(__file__).resolve().parent.parent.parent / "files" / f"{table_name}_{table_id}_{tg_id}.xlsx"

    if not file_path.exists():
        return await callback.message.answer(table_dose_not_exists_error)
    
    await callback.message.answer_document(document=FSInputFile(file_path), reply_markup = await get_actions_with_table_keyboard(table_id=table_id))

    os.remove(file_path)