# import re

# from aiogram import F, Router
# from aiogram.filters.state import StateFilter
# from aiogram.fsm.context import FSMContext
# from aiogram.types import CallbackQuery, Message
# from aiogram.fsm.state import State, StatesGroup

# from bot.keyboards.inline.table_keyboards import get_table_info_action_keyboard
# from bot.templates.messages_templates import (
#     enter_info_period_message,
#     table_base_info_message
# )
# from bot.templates.errors_templates import invalid_date_format_error
# from bot.templates.errors_templates import client_dose_not_exists_error
# from bot.templates.errors_templates import table_dose_not_exists_error
# from bot.database.tables.clients.dao import ClientDAO
# from bot.database.tables.dao import TableDAO
# from bot.utils.date_converter import get_date_for_db, parse_date
# from bot.utils.validators import is_valid_date

#router = Router()

# GET_STATISTIC_PATTERN = r"^get_clients_for_some_period_(\d+)_(.+)$"

# class Form(StatesGroup):
#     waiting_for_period_data = State()


# @router.callback_query(F.data.regexp(GET_STATISTIC_PATTERN))
# async def handle_period_table_info(callback: CallbackQuery, state: FSMContext):
#     await callback.answer()

#     match = re.match(GET_STATISTIC_PATTERN, callback.data)
#     table_id = int(match.group(1))
#     table_name = match.group(2)

#     table = await TableDAO.find_all(id=table_id, name = table_name)

#     if not table:
#         return await callback.message.answer(table_dose_not_exists_error)
    
#     clients = await ClientDAO.find_all(table_id = table_id)

#     if not clients:
#         return await callback.message.answer(client_dose_not_exists_error)
    
#     await callback.message.answer(enter_info_period_message(table_name=table_name))
    
#     await state.update_data(table_id=table_id, table_name=table_name)
#     await state.set_state(Form.waiting_for_period_data)

# @router.message(StateFilter(Form.waiting_for_period_data))
# async def handle_period(message: Message, state: FSMContext):
#     period_date = message.text.strip()

#     if not is_valid_date(period_date):
#         return await message.answer(invalid_date_format_error)
    
#     parsed_period_date = period_date.split('-')
#     date_from = parse_date(parsed_period_date[0])
#     date_to = parse_date(parsed_period_date[1])
    
#     data = await state.get_data()
#     table_id, table_name = data.get("table_id"), data.get("table_name")
    
#     table = await TableDAO.find_all(id=table_id, name=table_name)
#     if not table:
#         return await message.answer(table_dose_not_exists_error)
    
#     clients = await ClientDAO.find_all_by_period(
#         table_id=table_id,
#         date_from=date_from,
#         date_to=date_to
#     )

#     if not clients:
#         return await message.answer(client_dose_not_exists_error)
    
#     clients_count = len(clients)

#     all_prices = await ClientDAO.count_all_prices(
#         table_id=table_id, 
#         date_from=date_from, 
#         date_to=date_to
#     )

#     if not all_prices:
#         return await message.answer(client_dose_not_exists_error)

#     await message.answer(
#         table_base_info_message(
#             table_name=table_name, clients_count=clients_count, 
#             all_prices=all_prices, date_to=date_to, date_from=date_from
#         ),
#         reply_markup=await get_table_info_action_keyboard(table_id, table_name)
#     )
