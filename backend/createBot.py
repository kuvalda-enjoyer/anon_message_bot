from aiogram import Bot
import os
from dotenv import load_dotenv

load_dotenv()


def createBot():
    bot = Bot(token=os.getenv('TOKEN'))
    return bot