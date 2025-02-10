import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.database.tables.dao import TableDAO
from bot.keyboards.admin_keyboards.inline.table_keyboards import get_actions_with_table_keyboard
from bot.templates.admin_templates.errors_templates import table_dose_not_exists_error
from bot.templates.admin_templates.messages_templates import table_name_message

router = Router()

ACTIONS_WITH_TABLE_PATTERN = r"^get_(\d+)_table$"


@router.callback_query(F.data.regexp(ACTIONS_WITH_TABLE_PATTERN))
async def actions_with_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(ACTIONS_WITH_TABLE_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    message_sent = await callback.message.answer(
        table_name_message(table_name),
        reply_markup=await get_actions_with_table_keyboard(table_id=table_id),
    )

    await state.update_data(
        table_id=table_id,
        table_name=table_name,
        message_sent_id=callback.message.message_id,
    )
