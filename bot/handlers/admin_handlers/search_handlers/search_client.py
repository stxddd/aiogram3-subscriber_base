from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.database.clients.dao import ClientDAO
from bot.keyboards.admin_keyboards.inline.clients_keyboards import get_clients_for_edit
from bot.keyboards.admin_keyboards.inline.utils_keyboards import cancel_delete_last_keyboard

from bot.templates.admin_templates.messages_templates import (
    enter_query_text_message,
    clients_by_query_are_missing_message,
    clients_by_query_message
)
from bot.decorators.admin_required import admin_required
from bot.templates.admin_templates.keyboards_templates import searching_text


router = Router()

class Form(StatesGroup):
    waiting_for_query_text = State()

@router.message(F.text == searching_text)
@admin_required
async def handle_get_message_text(message: Message, state: FSMContext): 
    
    await state.set_state(Form.waiting_for_query_text)
    await message.answer(enter_query_text_message, reply_markup=cancel_delete_last_keyboard)
    
    
@router.message(StateFilter(Form.waiting_for_query_text))
@admin_required
async def handle_send_mailing(message: Message, state: FSMContext): 
    query = message.text
    
    clients = await ClientDAO.search_all(query = query)
    
    await state.clear()
    
    if not clients:  
        return await message.answer(clients_by_query_are_missing_message)
    
    return await message.answer(clients_by_query_message(query=query, length=len(clients)), reply_markup=await get_clients_for_edit(clients))
