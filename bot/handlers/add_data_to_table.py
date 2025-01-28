from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database.tables.lines.dao import LineDAO
from bot.keyboards.home import delete_last_keyboard, home_keyboard
from bot.templates.errors import adding_data_error
from bot.templates.messages import main_menu, new_data_added_message
from bot.utils.excel_generator import ExcelCRUD

router = Router()


class Form(StatesGroup):
    waiting_for_name_data = State()
    waiting_for_price_data = State()
    waiting_for_date_data = State()


@router.callback_query(F.data == "add_data_to_table")
async def add_line_to_table(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_sent = await callback.message.answer("Отправьте имя клиента", reply_markup=delete_last_keyboard)

    message_sent_id_actions_with_table = data.get("message_sent_id_actions_with_table")
    await callback.message.bot.delete_message(callback.message.chat.id, message_sent_id_actions_with_table)

    await callback.answer()
    await state.set_state(Form.waiting_for_name_data)
    await state.update_data(message_sent_id_name=message_sent.message_id)


@router.message(StateFilter(Form.waiting_for_name_data))
async def get_name(message: Message, state: FSMContext):
    name = message.text

    data = await state.get_data()
    message_sent_id_name = data.get("message_sent_id_name")
   
    message_sent = await message.answer("Отправьте цену услуги", reply_markup=delete_last_keyboard)

    await message.bot.delete_message(message.chat.id, message_sent_id_name)
    await state.update_data(name=name)
    await state.set_state(Form.waiting_for_price_data)
    await state.update_data(message_sent_id_price=message_sent.message_id)


@router.message(StateFilter(Form.waiting_for_price_data))
async def get_price(message: Message, state: FSMContext):
    price = message.text

    data = await state.get_data()
    message_sent_id_price = data.get("message_sent_id_price")
    

    message_sent = await message.answer(
        "Отправьте даты оказания услуг\ndd.mm.yyyy-dd.mm.yyyy",
        reply_markup=delete_last_keyboard,
    )

    await message.bot.delete_message(message.chat.id, message_sent_id_price)
    await state.update_data(price=price)
    await state.set_state(Form.waiting_for_date_data)
    await state.update_data(message_sent_id_date=message_sent.message_id)


@router.message(StateFilter(Form.waiting_for_date_data))
async def get_date(message: Message, state: FSMContext):
    data = await state.get_data()

    name = data.get("name")
    price = data.get("price")
    table_id = data.get("table_id")
    table_name = data.get("table_name")
    date = message.text

    new_line = await LineDAO.add(
        owner_tg_id=message.from_user.id,
        table_id=table_id,
        subscriber_tg_id=name,
        subscriber_price=price,
        subscriber_date=date,
    )

    if not new_line:
        return await message.answer(adding_data_error)

    new_excel_line = await ExcelCRUD.add_words_to_existing_excel(
        data=[name, price, date],
        table_id=table_id,
        tg_id=message.from_user.id,
        table_name=table_name,
    )

    if not new_excel_line:
        await LineDAO.delete(
            owner_tg_id=message.from_user.id,
            table_id=table_id,
            subscriber_tg_id=name,
            subscriber_price=price,
            subscriber_date=date,
        )
        return await message.answer(adding_data_error)

    success_message = await message.answer(f'{new_data_added_message}«{table_name}»\n\nКлиент: {name}\nЦена: {price}\nДаты: {date}')

    await state.update_data(date=date)
    message_sent_id_date = data.get("message_sent_id_date")
    await message.bot.delete_message(message.chat.id, message_sent_id_date)
    await state.update_data(message_ids=[success_message.message_id])
    await message.answer(main_menu, reply_markup=home_keyboard)
    await state.clear()
