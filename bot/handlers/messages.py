from aiogram import types

from bot.loader import dp
from bot.keyboards import *
from bot.states import UserStatesGroup, ManagerStatesGroup
from aiogram.dispatcher import FSMContext

from bot.db.database import db


# USER

# Обработка сообщений поиска услуг ремонта
@dp.message_handler(content_types=['text'], state=UserStatesGroup.search_repairs)
async def search_repairs(message: types.Message):
    ans, kb = get_found_repairs_keyboard(search_query=message.text)
    await message.answer(text=ans,
                         reply_markup=kb)


# Обработка сообщений поиска аксессуаров
@dp.message_handler(content_types=['text'], state=UserStatesGroup.search_accessories)
async def search_accessories(message: types.Message):
    ans, kb = get_found_accessories_keyboard(search_query=message.text)
    await message.answer(text=ans,
                         reply_markup=kb)


# MANAGER
