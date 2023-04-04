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
    if state == 'UserStatesGroup:repair_item':
        await UserStatesGroup.repair_item.set()
    if state == 'UserStatesGroup:accessories_catalog':
        await UserStatesGroup.accessories_catalog.set()
    if state == 'UserStatesGroup:accessories':
        await UserStatesGroup.accessories.set()


# USER

# Ветка ремонта

# Открыть каталог услуг
@dp.callback_query_handler(text='repairs_catalog', state=UserStatesGroup.start)
async def open_repairs_catalog(callback: types.CallbackQuery, state: FSMContext):
    await UserStatesGroup.repair.set()
    add_state(await state.get_state())
    ans, kb = get_repairs_catalog_keyboard()
    await callback.message.edit_text(text=ans,
                                     reply_markup=kb)
    await callback.answer()


# Открыть услугу
@dp.callback_query_handler(CallbackData('repairs_catalog', 'id', 'action').filter(), state=UserStatesGroup.repair)
async def open_repair_option(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await UserStatesGroup.repair_item.set()
        add_state(await state.get_state())
        ans, kb = get_repair_item_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Заказать услугу
@dp.callback_query_handler(CallbackData('repair_item', 'id', 'action').filter(), state=UserStatesGroup.repair_item)
async def make_an_order(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await UserStatesGroup.to_order.set()
        async with state.proxy() as data:
            data['repair_id'] = callback_data['id']
        add_state(await state.get_state())
        ans, kb = get_phone_models_category_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Выбрать категорию телефона
@dp.callback_query_handler(CallbackData('category_models', 'id', 'action').filter(), state=UserStatesGroup.to_order)
async def category_model_selection(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            ans, kb = get_keyboard(STATES_LIST[-2], service_id=data['repair_id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        add_state(await state.get_state())
        ans, kb = get_phone_models_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)


# Выбрать модель. Сформировать заказ
@dp.callback_query_handler(CallbackData('models', 'id', 'action').filter(), state=UserStatesGroup.to_order)
async def model_selection(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        async with state.proxy() as data:
            answer = db.insert_orders_repair(user_id=callback.from_user.id, repair_id=data['repair_id'], model_id=callback_data['id'])
        await callback.answer(answer)
        delete_all_states()
        await UserStatesGroup.start.set()
        add_state(await state.get_state())
        ans, kb = get_user_start_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Ветка аксессуаров

# Открыть каталог аксессуаров
@dp.callback_query_handler(text='accessories_catalog', state=UserStatesGroup.start)
async def open_accessories_catalog(callback: types.CallbackQuery, state: FSMContext):
    await UserStatesGroup.accessories_catalog.set()
    add_state(await state.get_state())
    ans, kb = get_accessories_catalog_keyboard()
    await callback.message.edit_text(text=ans,
                                     reply_markup=kb)
    await callback.answer()


# Открыть выбор аксессуара
@dp.callback_query_handler(CallbackData('accessories_catalog', 'id', 'action').filter(), state=UserStatesGroup.accessories_catalog)
async def open_accessories(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await UserStatesGroup.accessories.set()
        async with state.proxy() as data:
            data['catalog_id'] = callback_data['id']
        add_state(await state.get_state())
        ans, kb = get_accessories_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Открыть аксессуар
@dp.callback_query_handler(CallbackData('accessories', 'id', 'action').filter(), state=UserStatesGroup.accessories)
async def open_accessory(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await UserStatesGroup.accessory.set()
        add_state(await state.get_state())
        await callback.message.delete()
        ans, kb, photo = get_accessory_keyboard(callback_data['id'], callback.from_user.id)
        await callback.message.answer_photo(photo=photo,
                                            caption=ans[:1000],
                                            reply_markup=kb)
    await callback.answer()


# Добавить аксессуар в желаемое
@dp.callback_query_handler(CallbackData('accessory', 'id', 'action').filter(), state=UserStatesGroup.accessory)
async def open_accessory(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        await callback.message.delete()
        async with state.proxy() as data:
            ans, kb = get_keyboard(STATES_LIST[-2], catalog_id=data['catalog_id'])
        await callback.message.answer(text=ans,
                                      reply_markup=kb)
        delete_state()
    else:
        await callback.message.delete()
        db.insert_on_delete_desired(action=callback_data['action'], user_id=callback.from_user.id, accessory_id=callback_data['id'])
        ans, kb, photo = get_accessory_keyboard(callback_data['id'], callback.from_user.id)
        await callback.message.answer_photo(photo=photo,
                                            caption=ans[:1000],
                                            reply_markup=kb)
    await callback.answer()


# Ветка заказов

# Выбрать категорию заказов
@dp.callback_query_handler(text='orders', state=UserStatesGroup.start)
async def open_orders(callback: types.CallbackQuery):
    pass


# Ветка поиска

# Выбрать категорию поиска
@dp.callback_query_handler(text='repair_catalog', state=UserStatesGroup.start)
async def open_search(callback: types.CallbackQuery):
    pass


# Ветка о нас

# Открыть "О нас"
@dp.callback_query_handler(text='repair_catalog', state=UserStatesGroup.start)
async def open_about(callback: types.CallbackQuery):
    pass


# MANAGER
