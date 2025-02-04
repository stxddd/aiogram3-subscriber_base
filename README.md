**О проекте**

Aiogram + Postgresql (asyncpg + alembic)


🤖 Данный Бот создан для автоматизации ведения клиентской базы. Имейте постоянный доступ к своим базам, а Бот напомнит Вам, когда клиенту необходимо пополнить баланс.


**Для локальной установки**

Сделайте клон проекта 
```bash
git clone https://github.com/stxddd/aiogram3-subscriber_base.git
```

Задайте эти параметры в корневом .env 
```bash
TOKEN
DB_HOST
DB_PORT
DB_USER
DB_NAME
DB_PASS
MAX_TABLE_LIMIT
MAX_CLIENT_LIMIT 
DOWNLOAD_DAY_LIMIT 
TIME_TO_RECEIVE_NOTIFICATIONS 
```

Создаейте venv и установите зависимости
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Запустите bot/main.py
```bash
python -m bot.main
```