from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.templates.user_templates.keyboards_templates import(
    ios_os_text, 
    mac_os_text, 
    android_os_text, 
    windows_os_text, 
    android_tv_os_text,
    one_month_text,
    three_month_text,
    six_month_text,
    twelve_month_text,
) 
from bot.config import settings

enter_os_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [(InlineKeyboardButton(text=ios_os_text, callback_data='IOS_add_connection_os'))],
        [(InlineKeyboardButton(text=android_os_text, callback_data='Android_add_connection_os'))],
        [(InlineKeyboardButton(text=windows_os_text, callback_data='Windows_add_connection_os'))],
        [(InlineKeyboardButton(text=mac_os_text, callback_data='Mac_add_connection_os'))],
        [(InlineKeyboardButton(text=android_tv_os_text, callback_data='AndroidTV_add_connection_os'))],
    ],
    resize_keyboard=True,
)


enter_period_keyboard= InlineKeyboardMarkup(
    inline_keyboard=[
        [(InlineKeyboardButton(text=one_month_text, callback_data=f'1_{settings.ONE_MONTH_PRICE}_connection_period'))],
        [(InlineKeyboardButton(text=three_month_text, callback_data=f'3_{settings.THREE_MONTH_PRICE}_connection_period'))],
        [(InlineKeyboardButton(text=six_month_text, callback_data=f'6_{settings.SIX_MONTH_PRICE}_connection_period'))],
        [(InlineKeyboardButton(text=twelve_month_text, callback_data=f'12_{settings.ONE_YEAR_PRICE}_connection_period'))],
    ],
    resize_keyboard=True,
)

enter_extend_period_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [(InlineKeyboardButton(text=one_month_text, callback_data=f'1_{settings.ONE_MONTH_PRICE}_connection_period_extend'))],
        [(InlineKeyboardButton(text=three_month_text, callback_data=f'3_{settings.THREE_MONTH_PRICE}_connection_period_extend'))],
        [(InlineKeyboardButton(text=six_month_text, callback_data=f'6_{settings.SIX_MONTH_PRICE}_connection_period_extend'))],
        [(InlineKeyboardButton(text=twelve_month_text, callback_data=f'12_{settings.ONE_YEAR_PRICE}_connection_period_extend'))],
    ],
    resize_keyboard=True,
)