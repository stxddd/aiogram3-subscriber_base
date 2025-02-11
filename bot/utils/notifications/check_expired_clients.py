import asyncio
from datetime import datetime

from sqlalchemy import select

from bot.config import settings
from bot.database.database import async_session_maker
from bot.database.tables.clients.models import Client
from bot.database.tables.models import Table
from bot.database.users.dao import UserDAO
from bot.keyboards.admin_keyboards.inline.notification_keyboards import get_pay_info_keyboard
from bot.templates.admin_templates.messages_templates import client_date_to_expired


async def check_expired_clients(bot):
    while True:
        now = datetime.now().replace(
            hour=settings.HOUR_TO_RECEIVE_NOTIFICATIONS,
            minute=settings.MINUTE_TO_RECEIVE_NOTIFICATIONS,
            second=0,
            microsecond=0,
        )
        await asyncio.sleep((now - datetime.now()).total_seconds() % 86400)
        users = await UserDAO.find_all()

        async with async_session_maker() as session:
            today = datetime.today().date()
            for user in users:
                query = (
                    select(Client, Table)
                    .join(Table, Client.table_id == Table.id)
                    .where(Table.user_tg_id == user.tg_id)
                )
                result = await session.execute(query)
                clients = result.scalars().all()

                for client in clients:
                    client_date = client.date_to
                    if client_date and client_date < today:
                        message = await bot.send_message(
                            user.tg_id,
                            client_date_to_expired(
                                client_name=client.name, date_to=client.date_to
                            ),
                            reply_markup=await get_pay_info_keyboard(client_id=client.id),
                        )

                        await bot.pin_chat_message(user.tg_id, message.message_id)

        await asyncio.sleep(86400)
        
