from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.loader import dp

from bot.states import UserStatesGroup, ManagerStatesGroup
from bot.keyboards import *


# Переключатель состояний

async def set_state():

    # USER

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
    if state == 'UserStatesGroup:select_orders':
        await UserStatesGroup.select_orders.set()
    if state == 'UserStatesGroup:desired':
        await UserStatesGroup.desired.set()
    if state == 'UserStatesGroup:orders_repair':
        await UserStatesGroup.orders_repair.set()
    if state == 'UserStatesGroup:select_search':
        await UserStatesGroup.select_search.set()
    if state == 'UserStatesGroup:search_repairs':
        await UserStatesGroup.search_repairs.set()
    if state == 'UserStatesGroup:search_accessories':
        await UserStatesGroup.search_accessories.set()
    if state == 'UserStatesGroup:found_repair':
        await UserStatesGroup.found_repair.set()

    # MANAGER


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
        ans, kb = get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
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
        ans, kb = get_user_start_keyboard(callback.from_user.id)
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
        ans, kb = get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
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
    elif callback_data['action'] == 'sort_default' or callback_data['action'] == 'sort_asc' or callback_data['action'] == 'sort_desc':
        answer = set_sorting_answer(callback_data['action'])
        if answer[-1] != '!':
            async with state.proxy() as data:
                ans, kb = get_accessories_keyboard(data['catalog_id'])
            await callback.message.edit_text(text=ans,
                                             reply_markup=kb)
        await callback.answer(answer)
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

# Открыть выбор заказов
@dp.callback_query_handler(text='select_orders', state=UserStatesGroup.start)
async def open_select_orders(callback: types.CallbackQuery, state: FSMContext):
    await UserStatesGroup.select_orders.set()
    add_state(await state.get_state())
    ans, kb = get_select_orders_keyboard()
    await callback.message.edit_text(text=ans,
                                     reply_markup=kb)
    await callback.answer()


# Выбор заказов
@dp.callback_query_handler(CallbackData('select_orders', 'action').filter(), state=UserStatesGroup.select_orders)
async def select_orders(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    elif callback_data['action'] == 'desired':
        await UserStatesGroup.desired.set()
        add_state(await state.get_state())
        ans, kb = get_desired_keyboard(callback.from_user.id)
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    else:
        await UserStatesGroup.orders_repair.set()
        add_state(await state.get_state())
        ans, kb = get_orders_repair(callback.from_user.id)
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Выбор желаемого
@dp.callback_query_handler(CallbackData('desired', 'id', 'action').filter(), state=UserStatesGroup.desired)
async def select_desire(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await UserStatesGroup.desire.set()
        add_state(await state.get_state())
        await callback.message.delete()
        ans, kb, photo = get_accessory_keyboard(callback_data['id'], callback.from_user.id)
        await callback.message.answer_photo(photo=photo,
                                            caption=ans,
                                            reply_markup=kb)
    await callback.answer()


# Редактирование желаемого
@dp.callback_query_handler(CallbackData('accessory', 'id', 'action').filter(), state=UserStatesGroup.desire)
async def open_desire(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        await callback.message.delete()
        ans, kb = get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
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


# Выбор заказа услуги на ремонт
@dp.callback_query_handler(CallbackData('orders_repair', 'id', 'action').filter(), state=UserStatesGroup.orders_repair)
async def select_order_repair(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await UserStatesGroup.order_repair.set()
        add_state(await state.get_state())
        ans, kb = get_order_repair(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Заказ услуги на ремонт
@dp.callback_query_handler(CallbackData('order_repair', 'id', 'action').filter(), state=UserStatesGroup.order_repair)
async def order_repair(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        db.cancel_order_repair(order_id=callback_data['id'])
        await UserStatesGroup.orders_repair.set()
        ans, kb = get_orders_repair(callback.from_user.id)
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        await callback.answer('Заказ отменён!')
        delete_state()
    await callback.answer()


# Ветка поиска

# Открыть выбор категории поиска
@dp.callback_query_handler(text='select_search', state=UserStatesGroup.start)
async def open_select_search(callback: types.CallbackQuery, state: FSMContext):
    await UserStatesGroup.select_search.set()
    add_state(await state.get_state())
    ans, kb = get_select_search_keyboard()
    await callback.message.edit_text(text=ans,
                                     reply_markup=kb)


# Выбрать категорию поиска
@dp.callback_query_handler(CallbackData('select_search', 'action').filter(), state=UserStatesGroup.select_search)
async def select_search(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    elif callback_data['action'] == 'search_repair':
        await UserStatesGroup.search_repairs.set()
        add_state(await state.get_state())
        ans, kb = get_search_repairs_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    else:
        await UserStatesGroup.search_accessories.set()
        add_state(await state.get_state())
        ans, kb = get_search_accessories_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Вернуться из начала поиска услуг ремонта
@dp.callback_query_handler(CallbackData('search_repairs', 'action').filter(), state=UserStatesGroup.search_repairs)
async def back_search_repairs(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()


# Вернуться из начала поиска аксессуаров
@dp.callback_query_handler(CallbackData('search_accessories', 'action').filter(), state=UserStatesGroup.search_accessories)
async def back_search_accessories(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()


# Открыть услугу из поиска услуг
@dp.callback_query_handler(CallbackData('found_repairs', 'id', 'action').filter(), state=UserStatesGroup.search_repairs)
async def open_found_repair(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await UserStatesGroup.found_repair.set()
        add_state(await state.get_state())
        ans, kb = get_repair_item_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)


# Открыть аксессуар из поиска аксессуаров
@dp.callback_query_handler(CallbackData('found_accessories', 'id', 'action').filter(), state=UserStatesGroup.search_accessories)
async def open_found_accessory(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await UserStatesGroup.found_accessory.set()
        add_state(await state.get_state())
        ans, kb, photo = get_accessory_keyboard(callback_data['id'], callback.from_user.id)
        await callback.message.answer_photo(photo=photo,
                                            caption=ans,
                                            reply_markup=kb)


# Найденная услуга
@dp.callback_query_handler(CallbackData('repair_item', 'id', 'action').filter(), state=UserStatesGroup.found_repair)
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


# Найденный аксессуар
@dp.callback_query_handler(CallbackData('accessory', 'id', 'action').filter(), state=UserStatesGroup.found_accessory)
async def open_accessory(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        await callback.message.delete()
        ans, kb = get_keyboard(STATES_LIST[-2])
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


# Ветка о нас

# Открыть "О нас"
@dp.callback_query_handler(text='about', state=UserStatesGroup.start)
async def open_about(callback: types.CallbackQuery, state: FSMContext):
    await UserStatesGroup.about_module.set()
    add_state(await state.get_state())
    ans, kb = get_about_keyboard()
    await callback.message.edit_text(text=ans,
                                     reply_markup=kb)


# Вернуться из модуля "О нас"
@dp.callback_query_handler(CallbackData('about', 'action').filter(), state=UserStatesGroup.about_module)
async def back_about(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()


# Войти как мэнэджер
@dp.callback_query_handler(text='login_manager', state=UserStatesGroup.start)
async def open_about(callback: types.CallbackQuery):
    delete_all_states()
    db.change_status_id(user_id=callback.from_user.id, status_id=2)
    await callback.answer('Вы успешно вошли как мэнэджер!')
    await callback.message.delete()


# MANAGER
