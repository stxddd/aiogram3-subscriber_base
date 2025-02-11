from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.templates.user_templates.keyboards_templates import(
    ios_os_text, 
    mac_os_text, 
    android_os_text, 
    windows_os_text, 
    android_tv_os_text
) 

enter_os_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [(InlineKeyboardButton(text=ios_os_text, callback_data='IOS_add_connection'))],
        [(InlineKeyboardButton(text=android_os_text, callback_data='Android_add_connection'))],
        [(InlineKeyboardButton(text=windows_os_text, callback_data='Windows_add_connection'))],
        [(InlineKeyboardButton(text=mac_os_text, callback_data='Mac_add_connection'))],
        [(InlineKeyboardButton(text=android_tv_os_text, callback_data='AndroidTV_add_connection'))],
    ],
    resize_keyboard=True,
)
