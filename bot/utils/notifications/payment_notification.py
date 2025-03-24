import asyncio
import logging
from datetime import datetime, timedelta

from bot.config import settings
from bot.database.clients.dao import ClientDAO
from bot.database.connections.dao import ConnectionDAO
from bot.templates.user_templates.message_templates import you_need_to_pay_message

logger = logging.getLogger(__name__)

async def check_expired_clients(bot):
    while True:
        now = datetime.now()
        next_run = now.replace(
            hour=settings.HOUR_TO_RECEIVE_NOTIFICATIONS,
            minute=settings.MINUTE_TO_RECEIVE_NOTIFICATIONS,
            second=55,
            microsecond=0,
        )

        if now >= next_run:
            next_run += timedelta(days=1)

        sleep_time = (next_run - now).total_seconds()

        await asyncio.sleep(sleep_time)

        connections = await ConnectionDAO.find_all_with_marzban_link()
        today = datetime.today().date()

        for connection in connections:
            if connection.date_to - today <= timedelta(days=1):
                client = await ClientDAO.find_one_or_none(id=connection.client_id)
                if client:
                    await bot.send_message(
                        client.tg_id,
                        text=you_need_to_pay_message(connection=connection),
                    )

        await asyncio.sleep(86400)  
