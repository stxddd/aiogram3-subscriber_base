import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.database.tables.lines.dao import LineDAO
from bot.keyboards.tables import actions_with_table_keyboard

router = Router()


@router.callback_query(F.data.regexp(r"^get_(\d+)_(.+?)_table$"))
async def actions_with_table(callback: CallbackQuery, state: FSMContext):
    match = re.match(r"^get_(\d+)_(.+?)_table$", callback.data)
    await callback.answer()

    table_id = int(match.group(1))
    table_name = match.group(2)

    await state.update_data(table_id=table_id, table_name=table_name)

    message_sent = await callback.message.edit_text(
        f"Таблица: «{table_name}»", reply_markup=actions_with_table_keyboard
    )

    await state.update_data(message_sent_id_actions_with_table=message_sent.message_id)



