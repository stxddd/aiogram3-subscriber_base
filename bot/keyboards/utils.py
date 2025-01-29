from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.templates.keyboards import back_text, cancel_text

back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [(InlineKeyboardButton(text=back_text, callback_data="main_menu"))]
])

cancel_delete_last_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [(InlineKeyboardButton(text=cancel_text, callback_data="delete_last_message"))],
    ]
)
