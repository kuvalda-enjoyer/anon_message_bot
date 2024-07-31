import asyncio
from aiogram import Dispatcher, types
from aiogram.filters.command import Command
from backend.createBot import createBot


async def main():
    # Объект бота
    bot = createBot()
    # Диспетчер
    dp = Dispatcher(parse_mode="HTML")
    @dp.message(Command("start"))
    async def start(message: types.Message):
        await message.answer("Жопа какащке писи попи")
        
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())