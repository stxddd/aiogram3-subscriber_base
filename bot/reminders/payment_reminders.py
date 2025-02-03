import asyncio
from aiogram import Bot
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Model 


async def check_expired_models(session: AsyncSession, bot: Bot):
    today = date.today()
    


    for model in expired_models:
        message = f"Модель {model.name} истекла {model.end_date}"
        await bot.send_message(CHAT_ID, message)