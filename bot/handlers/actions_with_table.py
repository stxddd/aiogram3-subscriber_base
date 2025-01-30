import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.inline.tables import get_actions_with_table_keyboard
from bot.templates.messages import table_name_message

router = Router()


@router.callback_query(F.data.regexp(r"^get_(\d+)_(.+?)_table$"))
async def actions_with_table(callback: CallbackQuery, state: FSMContext):
    match = re.match(r"^get_(\d+)_(.+?)_table$", callback.data)
    await callback.answer()

    table_id = int(match.group(1))
    table_name = match.group(2)

    message_sent = await callback.message.answer(table_name_message(table_name), reply_markup = await get_actions_with_table_keyboard(table_id, table_name))

    await state.update_data(table_id=table_id, table_name=table_name, message_sent_id = callback.message.message_id)
    await state.update_data(message_sent_id_actions_with_table=message_sent.message_id)