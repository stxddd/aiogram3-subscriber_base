# **Project Overview**  
**Aiogram + PostgreSQL (asyncpg + alembic)**  

---
🤖 This bot (extension of the basic subscriber-base, which has full integration with the Marzban API) is capable of automatically connecting clients to a tunneled connection via your server for a certain period of time, on which Marzban has been installed. The administrator have access to all users and can distribute newsletters. Each individual user can't establish their own connections, subject to approval by the administrator.
---

## **Installation**  

Set the following environment variables:

```bash
TOKEN
ADMIN_TG_ID

MARZBAN_URL
MARZBAN_USER
MARZBAN_PASS
MARZBAN_REQUEST_DAY_LIMIT

POSTGRES_HOST
POSTGRES_PORT
POSTGRES_USER
POSTGRES_DB
POSTGRES_PASSWORD

ONE_MONTH_PRICE
THREE_MONTH_PRICE
SIX_MONTH_PRICE
ONE_YEAR_PRICE

CODE_KEY_FOR_DELETE

TZ=Europe/Moscow
```

### **Run Locally** 

```bash
python -m venv venv
venv\Scripts\activate  # For Windows  
source venv/bin/activate  # For Linux/macOS  
pip install -r requirements.txt
python -m bot.main
```
### **or**

To run the bot with Docker:
```bash
docker-compose up --build
```