from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from bot.templates.user_templates.keyboards_templates import get_instruction_text
from bot.templates.user_templates.message_templates import get_instruction_os_message
from bot.keyboards.user_keyboards.inline.instruction_keyboards import get_instruction_by_os_keyboard
from bot.keyboards.user_keyboards.reply.main_keyboards import main_keyboard
from bot.templates.user_templates.keyboards_templates import (
    android_os_text,
    android_tv_os_text,
    ios_os_text,
    mac_os_text,
    windows_os_text
)
from bot.templates.user_templates.message_templates import (
    android_instruction_message,
    windows_instruction_message,
    mac_instruction_message,
    androidTV_instruction_message,
    ios_instruction_message,
    incorrect_os_message
)

router = Router()

def get_instruction(user_os: str):
    if user_os == android_os_text: 
        return android_instruction_message
    elif user_os == android_tv_os_text:
        return androidTV_instruction_message
    elif user_os == ios_os_text:
        return ios_instruction_message
    elif user_os == mac_os_text:
        return mac_instruction_message
    elif user_os == windows_os_text:
        return windows_instruction_message
    return incorrect_os_message

@router.message(F.text == get_instruction_text)
async def handle_get_instruction(message: Message):
    return await message.answer(get_instruction_os_message, reply_markup = get_instruction_by_os_keyboard)

ADD_CONNECTION_PATTERN = '_get_instruction'

@router.callback_query(lambda c: c.data.endswith(ADD_CONNECTION_PATTERN))
async def handle_get_instruction(callback: CallbackQuery):
    await callback.answer()

    user_os = callback.data.split("_")[0] 
    return await callback.message.answer(get_instruction(user_os=user_os), reply_markup=main_keyboard)
    

    
