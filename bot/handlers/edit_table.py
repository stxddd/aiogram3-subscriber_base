from pathlib import Path
import re

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from bot.templates.messages import select_an_action_for_the_table
from bot.keyboards.inline.tables import get_edit_actions_with_table_keyboard

router = Router()

class Form(StatesGroup):
    waiting_for_name_data = State()


@router.callback_query(F.data.regexp(r"^edit_(\d+)_(.+)$"))
async def handle_edit_table_actions(callback: CallbackQuery):
    await callback.answer()

    match = re.match(r"^edit_(\d+)_(.+)$", callback.data)
    
    table_id = int(match.group(1))
    table_name = match.group(2)
    tg_id = callback.from_user.id

    await callback.message.answer(
        select_an_action_for_the_table(table_name),
        reply_markup = await get_edit_actions_with_table_keyboard
        (table_name=table_name, 
        table_id=table_id
    ))