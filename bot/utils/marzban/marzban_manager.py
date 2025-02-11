from random import randint

from marzban import MarzbanAPI, UserCreate, ProxySettings

from bot.config import settings

async def create_user(username: str):

    api = MarzbanAPI(base_url=settings.MARZBAN_URL)
    token = await api.get_token(username=settings.MARZBAN_USER, password=settings.MARZBAN_PASS)

    try:
        new_user = UserCreate(
            username=username, 
            proxies={"vless": ProxySettings(flow="xtls-rprx-vision")},
            inbounds={'vless': ['VLESS TCP REALITY']}
        )
        added_user = await api.add_user(user=new_user, token=token.access_token)
        await api.close()
        return added_user
    except: 
        await api.close()
        return None
   
        

async def get_user(username: str):
    try:
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
    except:
        return None           
       
 
 

   


    