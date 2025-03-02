import logging
from datetime import date, datetime

from marzban import MarzbanAPI, UserCreate, ProxySettings, UserModify
from bot.config import settings

logger = logging.getLogger(__name__)

async def create_user(username: str, date_to: date):
    api = MarzbanAPI(base_url=settings.MARZBAN_URL)
    
    try:
        token = await api.get_token(username=settings.MARZBAN_USER, password=settings.MARZBAN_PASS)
        date_to_datetime = datetime.combine(date_to, datetime.min.time())

        new_user = UserCreate(
            username=username, 
            proxies={"vless": ProxySettings(flow="xtls-rprx-vision")},
            inbounds={'vless': ['VLESS TCP REALITY']},
            expire=int(date_to_datetime.timestamp())
        )

        added_user = await api.add_user(user=new_user, token=token.access_token)
        return added_user

    except Exception as e:
        return None

    finally:
        await api.close()


async def get_user(username: str):
    api = MarzbanAPI(base_url=settings.MARZBAN_URL)

    try:
        token = await api.get_token(username=settings.MARZBAN_USER, password=settings.MARZBAN_PASS)
        user_info = await api.get_user(username=username, token=token.access_token)
        return user_info if user_info else None

    except Exception as e:
        return None

    finally:
        await api.close()


async def extend_user(username: str, date_to: date):
    api = MarzbanAPI(base_url=settings.MARZBAN_URL)

    try:
        token = await api.get_token(username=settings.MARZBAN_USER, password=settings.MARZBAN_PASS)
        new_expire = int(datetime.combine(date_to, datetime.min.time()).timestamp())

        user_data = UserModify(expire=new_expire)
        updated_user = await api.modify_user(username=username, token=token.access_token, user=user_data)

        return updated_user if updated_user else None

    except Exception as e:
        return None

    finally:
        await api.close()
