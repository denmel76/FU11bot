import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Ваш новый токен вписан напрямую
BOT_TOKEN = "9293135018:AAGIpCJyF8d7KrQGe9TUhC5PBf6C2Hn9_hA"

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
