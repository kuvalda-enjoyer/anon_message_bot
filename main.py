import asyncio
from aiogram import Dispatcher, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from backend.bot.createBot import createBot
from backend.states.state import SendingPost
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

bot = createBot()
dp = Dispatcher(parse_mode="HTML")

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Жопа какащке писи попи")

@dp.message(Command("send_post"))
async def send_post(message: Message, state: FSMContext):
    await message.answer("Напишите сообщение, которое хотите отправить")
    await state.set_state(SendingPost.GET_POST)

@dp.message(SendingPost.GET_POST)
async def confifm_post(message: Message, state: FSMContext):
    btns = [[KeyboardButton(text="Отправить✅"), KeyboardButton(text="Отменить❌")]]
    kb = ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f"Вы собираетесь отправить это сообщение:\r\n{message.text}", reply_markup=kb)
    if message.text == "Отправить✅":
        await state.update_data(post=message.text)
        await state.set_state(SendingPost.GET_CONFIRM)

# @dp.message(SendingPost.GET_CONFIRM)
# async def send_to_admin(message: Message, state: FSMContext):

   
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())