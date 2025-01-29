from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(F.data == "delete_last_message")
async def delete_last_message(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()