from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "delete_last_message")
async def handle_delete_last_message(callback: CallbackQuery, state: FSMContext):
    "Удаляет последнее сообщение и очищает state"
    await state.clear()
    await callback.message.delete()
