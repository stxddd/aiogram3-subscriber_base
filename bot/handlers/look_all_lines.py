from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.database.tables.lines.dao import LineDAO
from bot.keyboards.home import home_keyboard
from bot.keyboards.tables import actions_with_table_keyboard
from bot.database.tables.lines.dao import LineDAO
from bot.templates.messages import all_table_lines, main_menu, table_has_no_lines_message

router = Router()


@router.callback_query(F.data == 'look_all_lines')
async def actions_with_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    table_id, table_name, message_sent_id = data.get("table_id"), data.get("table_name"), data.get("message_sent_id")
    lines = await LineDAO.find_all(table_id=table_id)

    await callback.message.bot.delete_message(callback.message.chat.id, message_sent_id)

    if not lines:
        try:
            await callback.message.edit_text(table_has_no_lines_message(table_name), reply_markup=actions_with_table_keyboard)
        except:
            await callback.message.answer(table_has_no_lines_message(table_name))
    else:
        message_sent = await callback.message.answer(
            all_table_lines(lines, table_name), parse_mode="HTML"
        )
    await callback.message.answer(main_menu, reply_markup=home_keyboard)