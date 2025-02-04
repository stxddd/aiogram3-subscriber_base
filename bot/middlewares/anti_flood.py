import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.config import settings 
from bot.templates.messages_templates import anti_flood_message

FLOOD_THRESHOLD = settings.FLOOD_THRESHOLD

last_message_time: Dict[int, float] = {}

class AntiFloodMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()

        if user_id in last_message_time and current_time - last_message_time[user_id] < FLOOD_THRESHOLD:
            await event.answer(anti_flood_message)
            return  

        last_message_time[user_id] = current_time 
        return await handler(event, data) 