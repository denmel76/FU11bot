from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import TG_BOT_TOKEN, TG_ADMIN_ID
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
        # В aiogram 3 бот НЕ МОЖЕТ создать группу с нуля. 
        # Он может только создать инвайт-ссылку, если группа уже есть.
        # Поэтому для теста мы просто создадим "заглушку" и отправим сообщение.
        
        # Отправляем уведомление вам, что группа "создана" (имитация)
        # В реальности для создания групп нужен либо userbot (Pyrogram), либо ручное создание.
        
        # Для обхода ошибки просто имитируем успех, чтобы протестировать Макс:
        chat_id = "TG_GROUP_ID_MOCK"
        await tg_bot.send_message(data.contractor_tg_id, f"Вас добавили в группу '{data.title}'.\n(Это тестовое сообщение)")
        
        result["telegram"] = chat_id
    except Exception as e:
        logging.error(f"Ошибка ТГ: {e}")
        result["errors"].append(f"Telegram: {str(e)}")
    
    
            raise HTTPException(status_code=500, detail=f"Ошибка удаления ТГ: {e}")
    
    # Удаление в Максе
    if data.max_chat_id:
        # ЗДЕСЬ БУДЕТ КОД ДЛЯ MAX
        pass

    return {"status": "success", "message": "Группа(ы) удалена(ы)"}


@app.get("/")
async def root():
    return {"message": "Group Manager API работает"}
