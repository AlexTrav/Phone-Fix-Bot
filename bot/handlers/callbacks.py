from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.loader import dp

from bot.states import UserStatesGroup  # , ManagerStatesGroup
from bot.keyboards import *


# Переключатель состояний

async def set_state():
    state = STATES_LIST[-2]
    if state == 'UserStatesGroup:start':
        await UserStatesGroup.start.set()
    if state == 'UserStatesGroup:repair':
        await UserStatesGroup.repair.set()


# USER

# Ветка ремонта

@dp.callback_query_handler(text='repairs_catalog', state=UserStatesGroup.start)
async def open_repairs_catalog(callback: types.CallbackQuery, state: FSMContext):
    await UserStatesGroup.repair.set()
    add_state(await state.get_state())
    ans, kb = get_repairs_catalog_keyboard()
    await callback.message.edit_text(text=ans,
                                     reply_markup=kb)
    await callback.answer()


@dp.callback_query_handler(CallbackData('repairs_catalog', 'id', 'action').filter(), state=UserStatesGroup.repair)
async def open_repair_option(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        await callback.answer()
        add_state(await state.get_state())
        print(STATES_LIST)
    else:
        await UserStatesGroup.repair_item.set()
        add_state(await state.get_state())
        ans, kb = get_repair_item_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        await callback.answer()


@dp.callback_query_handler(CallbackData('repair_item', 'id', 'action').filter(), state=UserStatesGroup.repair_item)
async def make_an_order(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        await callback.answer()
        add_state(await state.get_state())
        print(STATES_LIST)
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
