from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.loader import dp, bot

from bot.states import UserStatesGroup, ManagerStatesGroup
from bot.keyboards import *

from bot.db.database import db


# Обработка команды "start"
@dp.message_handler(commands=['start'], state='*')
async def start_cmd(message: types.Message, state: FSMContext):
    db.check_user(user_id=message.from_user.id, user_name=message.from_user.username, fl_name=message.from_user.first_name + ' ' + message.from_user.last_name)
    status_id = db.get_status_id(user_id=message.from_user.id)
    delete_all_states()
    # USER
    if status_id == 1:
        await UserStatesGroup.start.set()
        add_state(await state.get_state())
        ans, kb = get_user_start_keyboard()
        await bot.send_message(chat_id=message.from_user.id,
                               text=ans,
                               reply_markup=kb)
    # MANAGER
    elif status_id == 2:
        await ManagerStatesGroup.start.set()
        add_state(state.get_state())
        ans, kb = get_manager_start_keyboard()
        await bot.send_message(chat_id=message.from_user.id,
                               text=kb,
                               reply_markup=ans)
