import asyncio
import os
from dotenv import load_dotenv
from typing import *
from aiogram import Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from backend.bot.createBot import createBot
from backend.states.state import SendingPost
from backend.classes.middleware import MediaMiddleware
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


bot = createBot()
load_dotenv()
ADMIN = os.getenv('ADMIN')
storage = MemoryStorage()
dp = Dispatcher(parse_mode="HTML", storage=storage)
orf_link = "\r\n\r\n(орф. сохранена)\r\n<a href='https://github.com/kuvalda-enjoyer/anon_message_bot'>Анонимная предложка</a>"

@dp.message(F.text, Command("start"))
async def start(message: types.Message, state: FSMContext):
    await message.answer("Вас приветствует анонимная предложка Базы ГУГР. Для отправки поста пришлите ваше сообщение.")
    await state.set_state(SendingPost.WAITING)

dp.message.middleware(MediaMiddleware(latency=0.01))

# отправка медиа группы
@dp.message(F.media_group_id != None, SendingPost.WAITING)
async def on_media_group_id(message: Message, state: FSMContext, media_events: List[Message] = []):
    m_capt = message.caption
    if m_capt == None:
        m_capt = ''
    m_capt = message.html_text+orf_link
    media_group = MediaGroupBuilder(caption=m_capt)
    for media_message in media_events:
        k = 0
        if media_message.photo:
            media_group.add(type="photo", media=media_message.photo[k].file_id)
        if media_message.video:
            media_group.add(type="video", media=media_message.video.file_id)
        if media_message.audio:
            media_group.add(type="audio", media=media_message.audio.file_id)
        k += 1

    await bot.send_message(ADMIN, "<i>В предложке появился новый пост!</i>")
    await bot.send_media_group(chat_id=ADMIN, media=media_group.build())
    await message.answer("Ваш пост отправлен в предложку!")
    await message.answer("Если хотите отправить ещё одно сообщение, просто напишите его")
    await state.set_state(SendingPost.WAITING)


# отправка текста
@dp.message(F.text, SendingPost.WAITING)
async def send_text(message: Message, state: FSMContext):
    msg = await message.send_copy(ADMIN)
    m_id = msg.message_id
    m_text = msg.html_text
    await bot.send_message(ADMIN, "<i>В предложке появился новый пост!</i>")
    await bot.edit_message_text(chat_id=ADMIN, message_id=m_id, text=f"{m_text}{orf_link}")
    await message.answer("Ваш пост отправлен в предложку!")
    await message.answer("Если хотите отправить ещё одно сообщение, просто напишите его")
    await state.set_state(SendingPost.WAITING)

# отправка файлов
@dp.message(SendingPost.WAITING)
async def send_text(message: Message, state: FSMContext):
    m_capt = message.caption
    if m_capt == None:
        m_capt = ''
    else:
        m_capt = message.html_text
    await bot.send_message(ADMIN, "<i>В предложке появился новый пост!</i>")
    msg = await message.copy_to(ADMIN)
    m_id = msg.message_id
    await bot.edit_message_caption(chat_id=ADMIN, message_id=m_id, caption=f"{m_capt}{orf_link}", parse_mode='html')
    await message.answer("Ваш пост отправлен в предложку!")
    await message.answer("Если хотите отправить ещё одно сообщение, просто напишите его")
    await state.set_state(SendingPost.WAITING)

   
async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())