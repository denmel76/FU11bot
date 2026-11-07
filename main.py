from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from aiogram import Bot

from config import TG_BOT_TOKEN, TG_ADMIN_ID

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# Инициализация бота ТГ
tg_bot = Bot(token=TG_BOT_TOKEN)

# --- МОДЕЛИ ДАННЫХ ---
class GroupCreateRequest(BaseModel):
    title: str
    description: str
    contractor_tg_id: int
    contractor_max_id: str = None 
    avatar_url: str = None

class GroupDeleteRequest(BaseModel):
    tg_chat_id: int = None
    max_chat_id: str = None

# --- ЭНДПОИНТЫ (API) ---

@app.post("/create_group")
async def create_group(data: GroupCreateRequest):
    result = {"telegram": None, "max": None, "errors": []}

    # 1. СОЗДАНИЕ В TELEGRAM (Имитация)
    try:
        await tg_bot.send_message(data.contractor_tg_id, f"Тест связи: группа '{data.title}' (создана имитация)")
        result["telegram"] = "TG_GROUP_ID_MOCK"
    except Exception as e:
        logging.error(f"Ошибка ТГ: {e}")
        result["errors"].append(f"Telegram: {str(e)}")

    # 2. СОЗДАНИЕ В МАКСЕ (Заглушка)
    if data.contractor_max_id:
        try:
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
            await tg_bot.leave_chat(data.tg_chat_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка удаления ТГ: {str(e)}")
    
    # Удаление в Максе
    if data.max_chat_id:
        pass

    return {"status": "success", "message": "Группа(ы) удалена(ы)"}

@app.get("/")
async def root():
    return {"message": "Group Manager API работает"}
