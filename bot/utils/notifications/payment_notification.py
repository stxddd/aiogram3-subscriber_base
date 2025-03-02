# import asyncio
# from datetime import datetime, timedelta

# from sqlalchemy import select

# from bot.config import settings
# from bot.database.connections.dao import ConnectionDAO
# from bot.database.database import async_session_maker
# from bot.database.clients.models import Client
# from bot.database.connections.models import Connection
# from bot.database.users.dao import UserDAO
# from bot.utils.messages import client_date_to_expired  # Убедись, что этот импорт корректен
# from bot.keyboards.inline import get_pay_info  # Убедись, что этот импорт корректен


# async def check_expired_clients(bot):
#     while True:

#         now = datetime.now()
#         target_time = now.replace(
#             hour=settings.HOUR_TO_RECEIVE_NOTIFICATIONS,
#             minute=settings.MINUTE_TO_RECEIVE_NOTIFICATIONS,
#             second=0,
#             microsecond=0,
#         )

#         if now > target_time:
#             target_time += timedelta(days=1)

#         await asyncio.sleep((target_time - now).total_seconds())

#         users = await UserDAO.find_all()

#         async with async_session_maker() as session:
#             today = datetime.today().date()
#             for user in users:
#                 query = (
#                     select(Connection, Client)
#                     .join(Client, Connection.client_id == Client.id)
#                     .where(Client.tg_id == user.tg_id)
#                 )
#                 result = await session.execute(query)
#                 connections = result.scalars().all()

#                 for connection in connections:
#                     client = await ConnectionDAO.find_one_or_none(id=connection.client_id)
#                     if connection.date_to and connection.date_to - today == timedelta(days=1):
#                         message = await bot.send_message(
#                             client.tg_id,
#                         )

#         await asyncio.sleep(86400)  
