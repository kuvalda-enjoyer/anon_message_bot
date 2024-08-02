import asyncio
from aiogram import router, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.state import SendingPost

@router.message(Command('send_post'))
async def send_post(message: Message, state: FSMContext):
    await message.answer("Напишите сообщение, которое хотите отправить")
    await state.set_state(SendingPost.GET_POST)