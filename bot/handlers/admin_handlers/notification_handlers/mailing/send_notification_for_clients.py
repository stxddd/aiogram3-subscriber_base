from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.database.clients.dao import ClientDAO
from bot.keyboards.admin_keyboards.inline.notification_keyboards import confirm_sending_keyboard
from bot.keyboards.admin_keyboards.inline.utils_keyboards import cancel_delete_last_keyboard

from bot.templates.admin_templates.messages_templates import (
    are_you_sure_to_send_mailing_message,
    enter_message_for_mailing_message
)
from bot.decorators.admin_required import admin_required
from bot.templates.admin_templates.keyboards_templates import mailing_text

router = Router()

SEND_MESSAGE_PATTERN = "send_message"


class Form(StatesGroup):
    waiting_for_message_text = State()


@router.message(F.text == mailing_text)
@admin_required
async def handle_get_message_text(message: Message, state: FSMContext): 
    await state.set_state(Form.waiting_for_message_text)
    await message.answer(enter_message_for_mailing_message, reply_markup=cancel_delete_last_keyboard)
    
    
@router.message(StateFilter(Form.waiting_for_message_text))
@admin_required
async def handle_send_mailing(message: Message, state: FSMContext): 
    text = message.text
    
    await state.update_data(text=text)
    return await message.answer(are_you_sure_to_send_mailing_message(message=text), reply_markup=await confirm_sending_keyboard())


@router.callback_query(F.data == SEND_MESSAGE_PATTERN)
@admin_required
async def actions_with_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    data = await state.get_data()
    text = data.get("text")
    
    clients = await ClientDAO.find_all()
    
    for client in clients:
        await callback.message.bot.send_message(client.tg_id, text)
