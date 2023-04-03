from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from os import getenv
from dotenv import load_dotenv, find_dotenv


# Подгрузка токена бота
load_dotenv(find_dotenv())


# Создание экземляров бота и диспетчера
bot = Bot(token=getenv('BOT_TOKEN_API'))
dp = Dispatcher(bot=bot, storage=MemoryStorage())
