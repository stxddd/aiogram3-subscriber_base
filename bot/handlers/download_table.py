from pathlib import Path

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from bot.keyboards.home import  home_keyboard
from bot.templates.errors import table_dose_not_exists_error
from bot.templates.messages import main_menu

router = Router()


@router.callback_query(F.data == "download_table")
async def download_table(callback: CallbackQuery, state: FSMContext):
    current_dir = Path(__file__).resolve().parent.parent

    await callback.answer()
    data = await state.get_data()

    message_sent_id_actions_with_table = data.get("message_sent_id_actions_with_table")
    await callback.message.bot.delete_message(
        callback.message.chat.id, message_sent_id_actions_with_table
    )

    table_id = data.get("table_id")
    table_name = data.get("table_name")
    tg_id = callback.from_user.id
    file_path = current_dir / "files" / f"{table_name}_{table_id}_{tg_id}.xlsx"

    if not file_path.exists():
        return await callback.message.edit_text(table_dose_not_exists_error)

    table = FSInputFile(file_path)

    sent_file_message = await callback.message.answer_document(document=table)
    await callback.message.answer(main_menu, reply_markup=home_keyboard)

    await state.update_data(message_ids=[sent_file_message.message_id])