from aiogram import types, Dispatcher
# from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData

from bot.loader import dp

from bot.states import UserStatesGroup, ManagerStatesGroup
from bot.keyboards import *


@dp.callback_query_handler(text='repairs_catalog', state=UserStatesGroup.start)
async def open_repair_catalog(callback: types.CallbackQuery):
    pass


@dp.callback_query_handler(text='accessories_catalog', state=UserStatesGroup.start)
async def open_accessories_catalog(callback: types.CallbackQuery):
    pass


@dp.callback_query_handler(text='orders', state=UserStatesGroup.start)
async def open_orders(callback: types.CallbackQuery):
    pass


@dp.callback_query_handler(text='repair_catalog', state=UserStatesGroup.start)
async def open_search(callback: types.CallbackQuery):
    pass


@dp.callback_query_handler(text='repair_catalog', state=UserStatesGroup.start)
async def open_about(callback: types.CallbackQuery):
    pass


