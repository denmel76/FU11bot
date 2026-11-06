import os

# Telegram
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_ADMIN_ID = int(os.environ.get("TG_ADMIN_ID", 0))

# Для Макса (если используем pymax, нужны данные аккаунта)
MAX_PHONE = os.environ.get("MAX_PHONE")
MAX_PASSWORD = os.environ.get("MAX_PASSWORD")
3. main.py (Сердце сервиса)

python
Copy
Download
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from aiogram import Bot
from aiogram.types import ChatPermissions
# from pymax import Client as MaxClient # Раскомментировать, когда будете готовы к Максу

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# Инициализация бота ТГ
tg_bot = Bot(token=TG_BOT_TOKEN)

# --- МОДЕЛИ ДАННЫХ (Что мы принимаем от CRM или вас) ---
class GroupCreateRequest(BaseModel):
    title: str
    description: str
    contractor_tg_id: int
    contractor_max_id: str = None # Пока опционально
    avatar_url: str = None

class GroupDeleteRequest(BaseModel):
    tg_chat_id: int = None
    max_chat_id: str = None

# --- ЭНДПОИНТЫ (API) ---

@app.post("/create_group")
async def create_group(data: GroupCreateRequest):
    result = {"telegram": None, "max": None, "errors": []}

    # 1. СОЗДАНИЕ В TELEGRAM
    try:
        # Создаем супергруппу
        group = await tg_bot.create_supergroup(title=data.title)
        chat_id = group.id
        
        # Ставим описание
        await tg_bot.set_chat_description(chat_id, data.description)
        
        # Настраиваем права (отключаем изменение инфо)
        await tg_bot.set_chat_permissions(
            chat_id, 
            permissions=ChatPermissions(
                can_send_messages=True, 
                can_change_info=False, 
                can_invite_users=True
            )
        )
        
        # Пишем сообщение-привязку
        await tg_bot.send_message(chat_id, f"Группа создана для заказа: {data.title}")

        # Приглашаем подрядчика
        invite_link = await tg_bot.create_chat_invite_link(chat_id, member_limit=1)
        await tg_bot.send_message(data.contractor_tg_id, f"Вас добавили в группу '{data.title}'.\nСсылка: {invite_link.invite_link}")

        result["telegram"] = chat_id
    except Exception as e:
        logging.error(f"Ошибка ТГ: {e}")
        result["errors"].append(f"Telegram: {str(e)}")

    # 2. СОЗДАНИЕ В МАКСЕ (Заглушка, пока нет библиотеки)
    if data.contractor_max_id:
        try:
            # ЗДЕСЬ БУДЕТ КОД ДЛЯ MAX
            # Пока просто имитируем успех
            result["max"] = "Группа создана (заглушка)"
        except Exception as e:
            result["errors"].append(f"Max: {str(e)}")

    if result["errors"]:
        return {"status": "partial_success", "data": result}
    
    return {"status": "success", "data": result}

@app.post("/delete_group")
async def delete_group(data: GroupDeleteRequest):
    # Удаление в ТГ
    if data.tg_chat_id:
        try:
            # В Telegram API нет прямого метода "удалить группу". 
            # Обычно бот выходит из группы (leave_chat), и если он был создателем, группа остается, но без админа.
            # Или можно использовать ban_chat_member для всех.
            await tg_bot.leave_chat(data.tg_chat_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка удаления ТГ: {e}")
    
    # Удаление в Максе
    if data.max_chat_id:
        # ЗДЕСЬ БУДЕТ КОД ДЛЯ MAX
        pass

    return {"status": "success", "message": "Группа(ы) удалена(ы)"}


@app.get("/")
async def root():
    return {"message": "Group Manager API работает"}
