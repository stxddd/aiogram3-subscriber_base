from pathlib import Path
import re

from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from bot.templates.errors import table_dose_not_exists_error
from bot.templates.messages import table_name_message

router = Router()


@router.callback_query(F.data.regexp(r"^download_table_(\d+)_(.+)$"))
async def handle_download_table(callback: CallbackQuery):
    match = re.match(r"^download_table_(\d+)_(.+)$", callback.data)
    await callback.answer()

    table_id = int(match.group(1))
    table_name = match.group(2)
    tg_id = callback.from_user.id

    file_path = Path(__file__).resolve().parent.parent / "files" / f"{table_name}_{table_id}_{tg_id}.xlsx"

    if not file_path.exists():
        return await callback.message.edit_text(table_dose_not_exists_error)

    await callback.message.answer(table_name_message(table_name))
    await callback.message.answer_document(document=FSInputFile(file_path))
