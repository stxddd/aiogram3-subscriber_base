import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings
from bot.handlers.admin_handlers.create_handlers.create_table import (
    router as create_table_router,
)
from bot.handlers.admin_handlers.delete_handlers.delete_client import (
    router as delete_client_router,
)
from bot.handlers.admin_handlers.delete_handlers.delete_table import (
    router as delete_table_router,
)
from bot.handlers.admin_handlers.edit_handlers.edit_table_name import (
    router as edit_table_name_router,
)
from bot.handlers.admin_handlers.get_handlers.get_clients_handlers.get_clients import (
    router as edit_clients_data_router,
)
from bot.handlers.admin_handlers.get_handlers.get_clients_handlers.get_connections import (
    router as get_connections_router,
)
from bot.handlers.admin_handlers.get_handlers.get_table_handlers.download_excel_table import (
    router as download_excel_table_router,
)
from bot.handlers.admin_handlers.get_handlers.get_table_handlers.get_tables import (
    router as get_tables_router,
)
from bot.handlers.admin_handlers.get_handlers.get_table_handlers.get_actions_about_table import (
    router as get_exel_table_by_id_router,
)
from bot.handlers.admin_handlers.notification_handlers.mailing.send_notification_for_clients import (
    router as send_notification_for_clients_router,
)
from bot.handlers.admin_handlers.notification_handlers.marzban.accept_extend_connection import (
    router as accept_extend_connection_router,
)
from bot.handlers.admin_handlers.notification_handlers.marzban.accept_marzban_client import (
    router as accept_marzban_client_router,
)
from bot.handlers.admin_handlers.notification_handlers.marzban.reject_extend_connection import (
    router as reject_extend_connection_router,
)
from bot.handlers.admin_handlers.notification_handlers.marzban.reject_marzban_client import (
    router as reject_marzban_client_router,
)
from bot.handlers.admin_handlers.search_handlers.search_client import (
    router as search_client_router,
)
from bot.handlers.base_handlers.delete_last_message import (
    router as delete_last_message_router,
)
from bot.handlers.base_handlers.start import router as base_commands_router
from bot.handlers.user_handlers.instruction_handlers.get_instructions import (
    router as get_instructions_router,
)
from bot.handlers.user_handlers.marzban_handlers.extend_marzban_link import (
    router as extend_marzban_link_router,
)
from bot.handlers.user_handlers.marzban_handlers.get_marzban_request import (
    router as handle_add_client_router,
)
from bot.utils.notifications.payment_notification import check_expired_clients

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_routers(
        base_commands_router,
        delete_last_message_router,
        get_instructions_router,
        
        get_tables_router,
        create_table_router,
        download_excel_table_router,
        
        edit_table_name_router,
        delete_table_router,
        
        handle_add_client_router,
        edit_clients_data_router,
        
        get_connections_router,
        delete_client_router,
        
        get_exel_table_by_id_router,
        
        send_notification_for_clients_router,
        
        search_client_router,
        extend_marzban_link_router,
        
        accept_marzban_client_router,
        reject_marzban_client_router,
        accept_extend_connection_router,
        reject_extend_connection_router,
    )

    asyncio.create_task(check_expired_clients(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
