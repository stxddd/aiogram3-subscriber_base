from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.templates.user_templates.keyboards_templates import(
    ios_os_text, 
    mac_os_text, 
    android_os_text, 
    windows_os_text, 
    android_tv_os_text
) 

get_instruction_by_os_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [(InlineKeyboardButton(text=ios_os_text, callback_data='IOS_get_instruction'))],
        [(InlineKeyboardButton(text=android_os_text, callback_data='Android_get_instruction'))],
        [(InlineKeyboardButton(text=windows_os_text, callback_data='Windows_get_instruction'))],
        [(InlineKeyboardButton(text=mac_os_text, callback_data='Mac_get_instruction'))],
        [(InlineKeyboardButton(text=android_tv_os_text, callback_data='AndroidTV_get_instruction'))],
    ],
    resize_keyboard=True,
)
