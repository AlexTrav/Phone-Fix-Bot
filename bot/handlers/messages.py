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

# Обработка сообщения добавления услуги ремонта
@dp.message_handler(content_types=['text'], state=ManagerStatesGroup.add_repair)
async def add_repair(message: types.Message):
    if message.text.count('\n') == 2:
        data = message.text.split('\n')
        db.add_repair(name=data[0], description=data[1], cost=data[2])
        delete_state()
        await ManagerStatesGroup.repairs_catalog.set()
        ans, kb = get_repairs_catalog_manager_keyboard()
        await message.answer(text=ans,
                             reply_markup=kb)
    else:
        await message.answer('Введены неверные данные')


# Обработка сообщения на редактирования поля услуги ремонта
@dp.message_handler(content_types=['text'], state=ManagerStatesGroup.update_field_repair)
async def update_field_repair(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        db.update_repair(field=data['field'], new_value=message.text, repair_id=data['repair_id'])
    delete_state()
    delete_state()
    await ManagerStatesGroup.repair_item.set()
    ans, kb = get_repair_item_manager_keyboard(data['repair_id'])
    await message.answer(text=ans,
                         reply_markup=kb)
