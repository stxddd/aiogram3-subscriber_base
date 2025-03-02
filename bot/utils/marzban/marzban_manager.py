from datetime import date, datetime

from marzban import MarzbanAPI, UserCreate, ProxySettings, UserModify

from bot.config import settings

async def create_user(username: str, date_to: date):

    api = MarzbanAPI(base_url=settings.MARZBAN_URL)
    token = await api.get_token(username=settings.MARZBAN_USER, password=settings.MARZBAN_PASS)
    
    date_to_datetime = datetime.combine(date_to, datetime.min.time())

    try:
        new_user = UserCreate(
            username=username, 
            proxies={"vless": ProxySettings(flow="xtls-rprx-vision")},
            inbounds={'vless': ['VLESS TCP REALITY']},
            expire=int(date_to_datetime.timestamp())

        )
        
        added_user = await api.add_user(user=new_user, token=token.access_token)
        
        await api.close()
        return added_user
    except: 
        await api.close()
        return None
   
   
async def get_user(username: str):
    api = MarzbanAPI(base_url=settings.MARZBAN_URL)
    token = await api.get_token(username=settings.MARZBAN_USER, password=settings.MARZBAN_PASS)
    
    try: 
        user_info = await api.get_user(username=username, token=token.access_token)
        
        await api.close()
        if not user_info:
            return None
        return user_info
    except: 
        await api.close()
        return None           
    

async def extend_user(username, date_to: date):
    api = MarzbanAPI(base_url=settings.MARZBAN_URL)
    token = await api.get_token(username=settings.MARZBAN_USER, password=settings.MARZBAN_PASS)
    
    try: 
        user_data = UserModify(expire=int(datetime.combine(date_to, datetime.min.time()).timestamp()))
        updated_user = await api.modify_user(username=username, token=token.access_token, user = user_data)
        await api.close()
        if not updated_user:
            return None
        return updated_user
    except: 
        await api.close()
        return None
        