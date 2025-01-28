from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "delete_last_message")
async def delete_last_message(callback: CallbackQuery):
    await callback.message.delete()