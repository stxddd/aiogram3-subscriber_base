# **Project Overview**  
**Aiogram + PostgreSQL (asyncpg + alembic)**  

🤖 This bot is designed to automate client database management. With constant access to your databases, the bot will notify you when a client needs to top up their balance.

---

## **Installation Instructions**  

Start by cloning the project:  
```bash
git clone https://github.com/stxddd/aiogram3-subscriber_base.git
```

Set the following environment variables:

```bash
TOKEN
DB_HOST  
DB_PORT  
DB_USER  
DB_NAME  
DB_PASS  
FLOOD_THRESHOLD  
MAX_TABLE_LIMIT  
MAX_CLIENT_LIMIT  
DOWNLOAD_DAY_LIMIT  
HOUR_TO_RECEIVE_NOTIFICATIONS
MINUTE_TO_RECEIVE_NOTIFICATIONS 
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