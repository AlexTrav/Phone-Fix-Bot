from aiogram import types, Dispatcher

from bot.loader import dp, bot

from bot.states import UserStatesGroup, ManagerStatesGroup
from bot.keyboards import *

from bot.db.database import db


@dp.message_handler(commands=['start'], state='*')
async def start_cmd(message: types.Message):
    db.check_user(user_id=message.from_user.id, user_name=message.from_user.username, fl_name=message.from_user.first_name + ' ' + message.from_user.last_name)
    status_id = db.get_status_id(user_id=message.from_user.id)
    # USER
    if status_id == 1:
        await UserStatesGroup.start.set()
        await bot.send_message(chat_id=message.from_user.id,
                               text='Добро пожаловать в Phone Fix Bot!',
                               reply_markup=get_user_start_keyboard())
    # MANAGER
    elif status_id == 2:
        await ManagerStatesGroup.start.set()
        await bot.send_message(chat_id=message.from_user.id,
                               text='Менеджер! Добро пожаловать в Phone Fix Bot!',
                               reply_markup=get_manager_start_keyboard())
