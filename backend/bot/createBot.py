from aiogram import Bot
import os
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

load_dotenv()


def createBot():
    bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    return bot