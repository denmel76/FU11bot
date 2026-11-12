import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TG_BOT_TOKEN

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я обновленный бот, запущенный с планшета!")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
