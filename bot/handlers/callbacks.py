from aiogram import types
# from aiogram.dispatcher import FSMContext

from bot.loader import dp

from bot.states import UserStatesGroup  # , ManagerStatesGroup
from bot.keyboards import *


# USER

# Ветка ремонта

@dp.callback_query_handler(text='repairs_catalog', state=UserStatesGroup.start)
async def open_repairs_catalog(callback: types.CallbackQuery):
    await UserStatesGroup.repair.set()
    await callback.message.edit_text(text='Выберите категорию ремонта:',
                                     reply_markup=get_repairs_catalog_keyboard())
    await callback.answer()


@dp.callback_query_handler(CallbackData('repairs_catalog', 'id', 'action').filter(), state=UserStatesGroup.repair)
async def open_repair_option(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        pass
        # await callback.message.edit_text(text=,
        #                                  reply_markup=)
        # await callback.answer()
    else:
        pass


# Ветка аксессуаров

@dp.callback_query_handler(text='accessories_catalog', state=UserStatesGroup.start)
async def open_accessories_catalog(callback: types.CallbackQuery):
    pass


# Ветка заказов

@dp.callback_query_handler(text='orders', state=UserStatesGroup.start)
async def open_orders(callback: types.CallbackQuery):
    pass


# Ветка поиска

@dp.callback_query_handler(text='repair_catalog', state=UserStatesGroup.start)
async def open_search(callback: types.CallbackQuery):
    pass


# Ветка о нас

@dp.callback_query_handler(text='repair_catalog', state=UserStatesGroup.start)
async def open_about(callback: types.CallbackQuery):
    pass


# MANAGER
