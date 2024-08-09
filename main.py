import asyncio
import os
from dotenv import load_dotenv
from aiogram import Dispatcher, types, F
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from backend.bot.createBot import createBot
from backend.states.state import SendingPost
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

bot = createBot()
load_dotenv()
ADMIN = os.getenv('ADMIN_ID')
dp = Dispatcher(parse_mode="HTML", storage=MemoryStorage())
orf_link = "\r\n\r\n(орф. сохранена)\r\n<a href='https://t.me/anon_predlozhka_gugr_bot'>Анонимная предложка</a>"

@dp.message(F.text, Command("start"))
async def start(message: types.Message):
    # kb_btns = [[KeyboardButton(text="ОТПРАВИТЬ ПОСТ✍️")]]
    # keyboard = ReplyKeyboardMarkup(keyboard=kb_btns, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Вас приветствует анонимная предложка Базы ГУГР. Для отправки поста пришлите команду /send_post.\r\nПока бот не принимает несколько медиафайлов за раз, просим прощения за неудобства.")

# F.text=='ОТПРАВИТЬ ПОСТ✍️'
@dp.message(F.text, Command("send_post"))
async def send_post(message: Message, state: FSMContext):
    await message.answer("Напишите сообщение, которое хотите отправить")
    await state.set_state(SendingPost.GET_POST)

# отправка текста
@dp.message(F.text, SendingPost.GET_POST)
async def send_text(message: Message, state: FSMContext):
    msg = await message.send_copy(ADMIN)
    m_id = msg.message_id
    m_text = msg.html_text
    await bot.edit_message_text(chat_id=ADMIN, message_id=m_id, text=f"{m_text}{orf_link}")
    await message.answer("Ваш пост отправлен в предложку!")
    await state.clear()

# отправка любых файлов
@dp.message(SendingPost.GET_POST)
async def send_text(message: Message, state: FSMContext):
    m_group = message.media_group_id
    m_capt = message.caption
    if m_capt == None:
        m_capt = ''
    else:
        m_capt = message.html_text
    await bot.send_message(ADMIN, "<i>В предложке появился новый пост!</i>")

    if m_group:
        await message.answer("ГОООООООЛ")
        # media = []
        # have_caption = False
        # for i in range(len(m_group)):
        #     if m_group[i][0] == "photo":
        #         media.append(InputMediaPhoto(media=m_group[i][1], caption=f"{m_capt}{orf_link}"))
        #     elif m_group[i][0] == "video":
        #         media.append(InputMediaVideo(media=m_group[i][1], caption=f"{m_capt}{orf_link}"))
        # # try:
        # await bot.send_media_group(chat_id=ADMIN, media=media)
        # await message.answer(media)
        # # except:
        # #     pass
    else:
        msg = await message.copy_to(ADMIN)
        m_id = msg.message_id
        await bot.edit_message_caption(chat_id=ADMIN, message_id=m_id, caption=f"{m_capt}{orf_link}", parse_mode='html')
        await message.answer("Ваш пост отправлен в предложку!")

    # m_id = msg.message_id
    # await bot.edit_message_caption(chat_id=ADMIN, message_id=m_id, caption=f"{m_capt}{orf_link}", parse_mode='html')
    await state.clear()

   
async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())