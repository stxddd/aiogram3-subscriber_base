import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from bot.database.clients.dao import ClientDAO
from bot.database.connections.dao import ConnectionDAO
from bot.keyboards.admin_keyboards.inline.utils_keyboards import (
    yes_or_not_delete_connection_keyboard, cancel_delete_last_keyboard
)
from bot.templates.admin_templates.errors_templates import (
    connection_does_not_exist_error,
    client_does_not_exists_error
)
from bot.templates.admin_templates.messages_templates import (
    are_you_sure_to_delete_connection_message,
    client_are_deleted_message,
    client_are_not_deleted_message,
    enter_code_for_delete_client,
    incorrect_code_message,
)
from bot.decorators.admin_required import admin_required
from bot.config import settings

router = Router()


class Form(StatesGroup):
    enter_secret_code_for_delete_client = State()


PREPARE_TO_DELETE_CLIENT_PATTERN = r"^prepare_to_delete_connection_(\d+)$"
DELETE_CLIENT_PATTERN = r"^delete_connection_(\d+)$"


@router.callback_query(F.data.regexp(PREPARE_TO_DELETE_CLIENT_PATTERN))
@admin_required
async def handle_prepare_to_delete_client(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(PREPARE_TO_DELETE_CLIENT_PATTERN, callback.data)
    connection_id = int(match.group(1))
    

    current_connection = await ConnectionDAO.find_by_id(connection_id)
    if not current_connection:
        return await callback.message.answer(connection_does_not_exist_error)
    
    current_client = await ClientDAO.find_by_id(current_connection.client_id)
    if not current_client:
        return await callback.message.answer(client_does_not_exists_error)
    
    await state.update_data(connection_id=connection_id)

    return await callback.message.answer(
        are_you_sure_to_delete_connection_message(
            client=current_client, connection=current_connection
        ),
        reply_markup=await yes_or_not_delete_connection_keyboard(connection_id=connection_id),
    )


@router.callback_query(F.data.regexp(DELETE_CLIENT_PATTERN))
@admin_required
async def handle_delete_client(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(DELETE_CLIENT_PATTERN, callback.data)
    connection_id = int(match.group(1))

    current_connection = await ConnectionDAO.find_by_id(connection_id)
    if not current_connection:
        return await callback.message.answer(connection_does_not_exist_error)
    
    current_client = await ClientDAO.find_by_id(current_connection.client_id)
    if not current_client:
        return await callback.message.answer(client_does_not_exists_error)
    
    await state.update_data(connection_id=connection_id)

    await state.set_state(Form.enter_secret_code_for_delete_client)
    return await callback.message.answer(
        enter_code_for_delete_client(client=current_client, connection=current_connection),
        reply_markup=cancel_delete_last_keyboard,
    )


@router.message(StateFilter(Form.enter_secret_code_for_delete_client))
async def handle_delete_secret_key(message: Message, state: FSMContext):
    code = message.text

    if code != settings.KEY_FOR_DELETE:
        await message.answer(incorrect_code_message)
    else:
        data = await state.get_data()
        connection_id = data.get("connection_id")

        current_connection = await ConnectionDAO.find_by_id(connection_id)
        if not current_connection:
            return await message.answer(connection_does_not_exist_error)
    
        current_client = await ClientDAO.find_by_id(current_connection.client_id)
        if not current_client:
            return await message.answer(client_does_not_exists_error)

        deleted_connection = await ConnectionDAO.delete(id=connection_id)

        if not deleted_connection:
            await message.answer(client_are_not_deleted_message(
                client=current_client
            ))

        await message.answer(client_are_deleted_message(
            client=current_client, connection=current_connection
        ))

        await state.clear()