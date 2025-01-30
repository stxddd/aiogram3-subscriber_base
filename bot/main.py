import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings
from bot.handlers.actions_with_table import  router as get_exel_table_by_id_router
from bot.handlers.handle_create_table import router as create_table_router
from bot.handlers.delete_last_message import router as delete_last_message_router
from bot.handlers.get_tables import router as get_tables_router
from bot.handlers.handle_start import router as base_commands_router
from bot.handlers.download_table import router as download_table_router
from bot.handlers.add_data_to_table import router as add_data_to_table_router
from bot.handlers.look_all_lines import router as look_all_lines_router

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_routers(
        base_commands_router,
        get_tables_router,
        create_table_router,
        get_exel_table_by_id_router,
        delete_last_message_router,
        download_table_router,
        add_data_to_table_router,
        look_all_lines_router
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass