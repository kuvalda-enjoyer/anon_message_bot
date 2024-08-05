import asyncio
import os
from dotenv import load_dotenv
from aiogram import Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from backend.bot.createBot import createBot
from backend.states.state import SendingPost
from aiogram.fsm.storage.memory import MemoryStorage

bot = createBot()
load_dotenv()
ADMIN = os.getenv('ADMIN_ID')
dp = Dispatcher(parse_mode="HTML", storage=MemoryStorage())
orf_link = "\r\n(орф. сохранена)\r\n<a href='https://t.me/anon_predlozhka_gugr_bot'>Анонимная предложка</a>"

@dp.message(F.text, Command("start"))
async def start(message: types.Message):
    await message.answer("Жопа какащке писи попи")

@dp.message(F.text, Command("send_post"))
async def send_post(message: Message, state: FSMContext):
    await state.set_state(SendingPost.START)
    await message.answer("Напишите сообщение, которое хотите отправить")
    await state.set_state(SendingPost.GET_POST)

@dp.message(F.text, SendingPost.GET_POST)
async def confifm_post(message: Message, state: FSMContext):
    await state.update_data(post=message.text)
    context_data = await state.get_data()
    post = context_data.get('post')
    await bot.send_message(ADMIN, "<i>В предложке появился новый пост!</i>")
    await bot.send_message(ADMIN, f"{post}{orf_link}")
    await message.answer("Ваш пост отправлен в предложку!")
    await state.clear()

   
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())