import re

from aiogram import F, Router
from aiogram.types import Message

from bot.database.clients.dao import ClientDAO
from bot.database.connections.dao import ConnectionDAO
from bot.keyboards.admin_keyboards.inline.clients_keyboards import get_actions_with_table_keyboard
from bot.templates.admin_templates.errors_templates import clients_does_not_exists_error
from bot.templates.admin_templates.messages_templates import table_name_message
from bot.decorators.admin_required import admin_required
from bot.templates.admin_templates.keyboards_templates import my_clients_text

router = Router()


@router.message(F.text == my_clients_text)
@admin_required
async def actions_with_clients(message: Message):   
    
    clients = await ClientDAO.find_all()
    
    if not clients:
        return await message.answer(
            clients_does_not_exists_error
        )
    
    await message.answer(
        table_name_message(),
        reply_markup=await get_actions_with_table_keyboard(),
    )
