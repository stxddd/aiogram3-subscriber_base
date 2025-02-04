import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings
from bot.handlers.base_handlers.start import router as base_commands_router
from bot.handlers.delete_handlers.delete_line import \
    router as delete_line_router
from bot.handlers.delete_handlers.delete_table import \
    router as delete_table_router
from bot.handlers.edit_table_data_handlers.edit_data_date_from import \
    router as edit_data_date_from_router
from bot.handlers.edit_table_data_handlers.edit_data_date_to import \
    router as edit_data_date_to_router
from bot.handlers.edit_table_data_handlers.edit_data_name import \
    router as edit_data_name_router
from bot.handlers.edit_table_data_handlers.edit_data_price import \
    router as edit_data_price_router
from bot.handlers.edit_table_data_handlers.edit_lines_data import \
    router as edit_table_data_router
from bot.handlers.edit_table_handlers.edit_table import \
    router as edit_table_router
from bot.handlers.edit_table_handlers.edit_table_name import \
    router as edit_table_name_router
from bot.handlers.get_handlers.actions_with_table import \
    router as get_exel_table_by_id_router
from bot.handlers.get_handlers.download_table import \
    router as download_table_router
from bot.handlers.get_handlers.get_tables import router as get_tables_router
from bot.handlers.get_handlers.look_all_lines import \
    router as look_all_lines_router
from bot.handlers.info_handlers.get_table_info import \
    router as get_table_info_router
from bot.handlers.notification_handlers.payment_completed import \
    router as payment_completed_router
from bot.handlers.notification_handlers.payment_didnt_completed import \
    router as payment_didnt_completed_router
from bot.handlers.post_handlers.add_data_to_table import \
    router as add_data_to_table_router
from bot.handlers.post_handlers.create_table import \
    router as create_table_router
from bot.handlers.utils_hadnlers.delete_last_message import \
    router as delete_last_message_router
from bot.middlewares.anti_flood import AntiFloodMiddleware
from bot.utils.notifications.check_expired_clients import check_expired_clients

logging.basicConfig(level=logging.INFO)


bot = Bot(
    token=settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

#dp.message.middleware(AntiFloodMiddleware())
#dp.callback_query.middleware(AntiFloodMiddleware())

async def main():
    dp.include_routers(
        base_commands_router,
        get_tables_router,
        create_table_router,
        get_exel_table_by_id_router,
        delete_last_message_router,
        add_data_to_table_router,
        look_all_lines_router,
        edit_table_router,
        edit_table_name_router,
        delete_table_router,
        delete_line_router,
        edit_table_data_router,
        edit_data_name_router,
        edit_data_price_router,
        edit_data_date_from_router,
        edit_data_date_to_router,
        get_table_info_router,
        download_table_router,
        payment_completed_router,
        payment_didnt_completed_router,
    )

    asyncio.create_task(check_expired_clients(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
