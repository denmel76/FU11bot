import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Токен вписан напрямую, чтобы не зависеть от config.py
BOT_TOKEN = "9156594719:AAEv56NLlQaeq7RafJtHBBEVctpsvwEpnVQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я обновленный бот, запущенный с планшета!")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
