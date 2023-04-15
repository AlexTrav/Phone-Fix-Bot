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
    # Ветка услуг ремонта
    if state == 'UserStatesGroup:repair':
        await UserStatesGroup.repair.set()
    if state == 'UserStatesGroup:repair_item':
        await UserStatesGroup.repair_item.set()
    # Ветка аксессуаров
    if state == 'UserStatesGroup:accessories_catalog':
        await UserStatesGroup.accessories_catalog.set()
    if state == 'UserStatesGroup:accessories':
        await UserStatesGroup.accessories.set()
    # Ветка заказов
    if state == 'UserStatesGroup:select_orders':
        await UserStatesGroup.select_orders.set()
    if state == 'UserStatesGroup:desired':
        await UserStatesGroup.desired.set()
    if state == 'UserStatesGroup:orders_repair':
        await UserStatesGroup.orders_repair.set()
    # Ветка поиска
    if state == 'UserStatesGroup:select_search':
        await UserStatesGroup.select_search.set()
    if state == 'UserStatesGroup:search_repairs':
        await UserStatesGroup.search_repairs.set()
    if state == 'UserStatesGroup:search_accessories':
        await UserStatesGroup.search_accessories.set()
    if state == 'UserStatesGroup:found_repair':
        await UserStatesGroup.found_repair.set()

    # MANAGER
    if state == 'ManagerStatesGroup:start':
        await ManagerStatesGroup.start.set()
    # Ветка услуг ремонта
    if state == 'ManagerStatesGroup:repairs_catalog':
        await ManagerStatesGroup.repairs_catalog.set()
    if state == 'ManagerStatesGroup:repair_item':
        await ManagerStatesGroup.repair_item.set()
    if state == 'ManagerStatesGroup:update_repair':
        await ManagerStatesGroup.update_repair.set()
    if state == 'ManagerStatesGroup:orders_repair':
        await ManagerStatesGroup.orders_repair.set()
    # Ветка аксессуаров
    if state == 'ManagerStatesGroup:accessories_catalog':
        await ManagerStatesGroup.accessories_catalog.set()
    if state == 'ManagerStatesGroup:accessories':
        await ManagerStatesGroup.accessories.set()
    if state == 'ManagerStatesGroup:accessory':
        await ManagerStatesGroup.accessory.set()
    if state == 'ManagerStatesGroup:update_accessory':
        await ManagerStatesGroup.update_accessory.set()
    if state == 'ManagerStatesGroup:desired_accessories':
        await ManagerStatesGroup.desired_accessories.set()
    # Ветка пользователей
    if state == 'ManagerStatesGroup:users':
        await ManagerStatesGroup.users.set()
    if state == 'ManagerStatesGroup:user':
        await ManagerStatesGroup.user.set()

    # Ветка документов


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
        ans, kb = get_orders_repair_keyboard(callback.from_user.id)
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
        ans, kb = get_order_repair_keyboard(callback_data['id'])
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
        ans, kb = get_orders_repair_keyboard(callback.from_user.id)
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
    await callback.answer()


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
    await callback.answer()


# Вернуться из начала поиска аксессуаров
@dp.callback_query_handler(CallbackData('search_accessories', 'action').filter(), state=UserStatesGroup.search_accessories)
async def back_search_accessories(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    await callback.answer()


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
    await callback.answer()


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
    await callback.answer()


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
    await callback.answer()


# Вернуться из модуля "О нас"
@dp.callback_query_handler(CallbackData('about', 'action').filter(), state=UserStatesGroup.about_module)
async def back_about(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2], user_id=callback.from_user.id)
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    await callback.answer()


# Войти как менеджер
@dp.callback_query_handler(text='login_manager', state=UserStatesGroup.start)
async def open_about(callback: types.CallbackQuery):
    delete_all_states()
    db.change_status_id(user_id=callback.from_user.id, status_id=2)
    await callback.answer('Вы успешно вошли как менеджер!')
    await callback.message.delete()
    await callback.answer()


# MANAGER

# Ветка услуг ремонта

# Открыть услуги ремонта
@dp.callback_query_handler(text='repairs_catalog', state=ManagerStatesGroup.start)
async def open_repairs_catalog(callback: types.CallbackQuery, state: FSMContext):
    await ManagerStatesGroup.repairs_catalog.set()
    add_state(await state.get_state())
    ans, kb = get_repairs_catalog_manager_keyboard()
    await callback.message.edit_text(text=ans,
                                     reply_markup=kb)
    await callback.answer()


# Выбрать / Добавить услугу ремонта / Открыть заказанные услуги
@dp.callback_query_handler(CallbackData('repairs_catalog', 'id', 'action').filter(), state=ManagerStatesGroup.repairs_catalog)
async def repairs_catalog(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    elif callback_data['action'] == 'add':
        await ManagerStatesGroup.add_repair.set()
        add_state(await state.get_state())
        ans, kb = get_add_repair_item_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    elif callback_data['action'] == 'orders_repair':
        await ManagerStatesGroup.orders_repair.set()
        add_state(await state.get_state())
        ans, kb = get_orders_repair_manager_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    else:
        await ManagerStatesGroup.repair_item.set()
        add_state(await state.get_state())
        ans, kb = get_repair_item_manager_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Вернуться из добавление услуги ремонта
@dp.callback_query_handler(CallbackData('repair_item', 'action').filter(), state=ManagerStatesGroup.add_repair)
async def back_add_repair(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Удаление / Выбор редактирования услуги ремонта
@dp.callback_query_handler(CallbackData('repair_item', 'id', 'action').filter(), state=ManagerStatesGroup.repair_item)
async def back_add_repair(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    elif callback_data['action'] == 'delete':
        db.delete_repair(repair_id=callback_data['id'])
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
        await callback.answer('Услуга ремонта успешно удалена!')
    else:
        await ManagerStatesGroup.update_repair.set()
        add_state(await state.get_state())
        async with state.proxy() as data:
            data['repair_id'] = callback_data['id']
        ans, kb = get_update_repair_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Выбор поля на редактирование услуги ремонта
@dp.callback_query_handler(CallbackData('update_repair', 'action').filter(), state=ManagerStatesGroup.update_repair)
async def select_field_update_repair(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            ans, kb = get_keyboard(STATES_LIST[-2], repair_id=data['repair_id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await ManagerStatesGroup.update_field_repair.set()
        add_state(await state.get_state())
        async with state.proxy() as data:
            data['field'] = callback_data['action']
        ans, kb = get_update_field_repair_keyboard(callback_data['action'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Вернуться из редактирования услуги ремонта
@dp.callback_query_handler(CallbackData('update_field_repair', 'action').filter(), state=ManagerStatesGroup.update_field_repair)
async def back_update_field_repair(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    await callback.answer()


# Выбор заказанной услуги ремнота
@dp.callback_query_handler(CallbackData('orders_repair', 'id', 'action').filter(), state=ManagerStatesGroup.orders_repair)
async def select_order_repair(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await ManagerStatesGroup.order_repair.set()
        add_state(await state.get_state())
        db.change_is_processed(order_repair_id=callback_data['id'])
        ans, kb = get_order_repair_manager_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Обработка заказа услуги ремонта
@dp.callback_query_handler(CallbackData('order_repair', 'id', 'action').filter(), state=ManagerStatesGroup.order_repair)
async def select_order_repair(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    elif callback_data['action'] == 'execute':
        db.change_is_completed(order_repair_id=callback_data['id'])
        ans, kb = get_order_repair_manager_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        await callback.answer('Заказ выполнен!')
    else:
        db.cancel_order_repair(order_id=callback_data['id'])
        delete_state()
        await ManagerStatesGroup.orders_repair.set()
        ans, kb = get_orders_repair_manager_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        await callback.answer('Заказ отменён!')
    await callback.answer()


# Ветка аксессуаров

# Открыть каталог акссесуаров
@dp.callback_query_handler(text='accessories_catalog', state=ManagerStatesGroup.start)
async def open_accessories_catalog(callback: types.CallbackQuery, state: FSMContext):
    await ManagerStatesGroup.accessories_catalog.set()
    add_state(await state.get_state())
    ans, kb = get_accessories_catalog_manager_keyboard()
    await callback.message.edit_text(text=ans,
                                     reply_markup=kb)
    await callback.answer()


# Выбрать / Добавить / Удалить категорию аксессуаров / Открыть желаемые товары
@dp.callback_query_handler(CallbackData('accessories_catalog', 'id', 'action').filter(), state=ManagerStatesGroup.accessories_catalog)
async def accessories_catalog(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    elif callback_data['action'] == 'add':
        await ManagerStatesGroup.add_accessory_catalog.set()
        add_state(await state.get_state())
        ans, kb = get_add_accessory_catalog_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    elif callback_data['action'] == 'desired':
        await ManagerStatesGroup.desired_accessories.set()
        add_state(await state.get_state())
        ans, kb = get_desired_manager_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    elif callback_data['action'] == 'delete':
        await ManagerStatesGroup.delete_accessory_catalog.set()
        add_state(await state.get_state())
        ans, kb = get_delete_accessory_catalog_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    else:
        await ManagerStatesGroup.accessories.set()
        add_state(await state.get_state())
        async with state.proxy() as data:
            data['category_id_manager'] = callback_data['id']
        ans, kb = get_accessories_manager_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Вернуться из добавление категории аксессуаров
@dp.callback_query_handler(CallbackData('add_accessory_catalog', 'action').filter(), state=ManagerStatesGroup.add_accessory_catalog)
async def back_add_accessory_catalog(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    await callback.answer()


# Выбор категории аксессуаров на удаление
@dp.callback_query_handler(CallbackData('delete_accessory_catalog', 'id', 'action').filter(), state=ManagerStatesGroup.delete_accessory_catalog)
async def delete_accessory_catalog(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        db.delete_accessory_catalog(accessory_catalog_id=callback_data['id'])
        delete_state()
        await ManagerStatesGroup.accessories_catalog.set()
        ans, kb = get_accessories_catalog_manager_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        await callback.answer('Категория успешно удалена!')
    await callback.answer()


# Выбрать / Добавить аксессуар
@dp.callback_query_handler(CallbackData('accessories', 'id', 'action').filter(), state=ManagerStatesGroup.accessories)
async def accessories(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    elif callback_data['action'] == 'add':
        await ManagerStatesGroup.add_accessory.set()
        add_state(await state.get_state())
        ans, kb = get_add_accessory_keyboard()
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    else:
        await ManagerStatesGroup.accessory.set()
        add_state(await state.get_state())
        await callback.message.delete()
        ans, kb, photo = get_accessory_manager_keyboard(callback_data['id'])
        await callback.message.answer_photo(photo=photo,
                                            caption=ans,
                                            reply_markup=kb)
    await callback.answer()


# Вернуться из добавления аксессуара
@dp.callback_query_handler(CallbackData('add_accessory', 'action').filter(), state=ManagerStatesGroup.add_accessory)
async def back_add_accessory(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        async with state.proxy() as data:
            ans, kb = get_keyboard(STATES_LIST[-2], category_id=data['category_id_manager'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    await callback.answer()


# Удалить аксессуар / Выбор редактирования аксессуара
@dp.callback_query_handler(CallbackData('accessory', 'id', 'action').filter(), state=ManagerStatesGroup.accessory)
async def accessory(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await callback.message.delete()
        await set_state()
        async with state.proxy() as data:
            ans, kb = get_keyboard(STATES_LIST[-2], category_id=data['category_id_manager'])
        await callback.message.answer(text=ans,
                                      reply_markup=kb)
        delete_state()
    elif callback_data['action'] == 'update':
        await ManagerStatesGroup.update_accessory.set()
        await callback.message.delete()
        add_state(await state.get_state())
        async with state.proxy() as data:
            data['accessory_id'] = callback_data['id']
        ans, kb = get_update_accessory_keyboard()
        await callback.message.answer(text=ans,
                                      reply_markup=kb)
    else:
        db.delete_accessory(accessory_id=callback_data['id'])
        await set_state()
        async with state.proxy() as data:
            ans, kb = get_keyboard(STATES_LIST[-2], category_id=data['category_id_manager'])
        await callback.message.answer(text=ans,
                                      reply_markup=kb)
        delete_state()
        await callback.answer('Аксессуар успешно удалён!')
        await callback.message.delete()
    await callback.answer()


# Выбор поля на редактирование аксессуара
@dp.callback_query_handler(CallbackData('update_accessory', 'action').filter(), state=ManagerStatesGroup.update_accessory)
async def select_field_update_accessory(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await callback.message.delete()
        await set_state()
        async with state.proxy() as data:
            ans, kb, photo = get_keyboard(STATES_LIST[-2], accessory_id=data['accessory_id'])
        await callback.message.answer_photo(photo=photo,
                                            caption=ans,
                                            reply_markup=kb)
        delete_state()
    else:
        await ManagerStatesGroup.update_field_accessory.set()
        add_state(await state.get_state())
        async with state.proxy() as data:
            data['field'] = callback_data['action']
        ans, kb = get_update_field_accessory_keyboard(callback_data['action'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Вернуться из редактирования услуги ремонта
@dp.callback_query_handler(CallbackData('update_field_accessory', 'action').filter(), state=ManagerStatesGroup.update_field_accessory)
async def back_update_field_accessory(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    await callback.answer()


# Выбор из желаемых аксессуаров
@dp.callback_query_handler(CallbackData('desired_accessories', 'id', 'action').filter(), state=ManagerStatesGroup.desired_accessories)
async def desired_accessories(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await ManagerStatesGroup.desired_accessory.set()
        add_state(await state.get_state())
        await callback.message.delete()
        ans, kb, photo = get_desired_accessory_manager_keyboard(callback_data['id'])
        await callback.message.answer_photo(photo=photo,
                                            caption=ans,
                                            reply_markup=kb)
    await callback.answer()


# Вернуться из желаемого аксессуара
@dp.callback_query_handler(CallbackData('desired_accessory', 'action').filter(), state=ManagerStatesGroup.desired_accessory)
async def back_desired_accessory(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        await callback.message.delete()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.answer(text=ans,
                                      reply_markup=kb)
        delete_state()
    await callback.answer()


# Ветка пользователей

# Открыть меню пользователей
@dp.callback_query_handler(text='users', state=ManagerStatesGroup.start)
async def open_users(callback: types.CallbackQuery, state: FSMContext):
    await ManagerStatesGroup.users.set()
    add_state(await state.get_state())
    ans, kb = get_users_keyboard()
    await callback.message.edit_text(text=ans,
                                     reply_markup=kb)
    await callback.answer()


# Выбор пользователя
@dp.callback_query_handler(CallbackData('users', 'id', 'action').filter(), state=ManagerStatesGroup.users)
async def open_user(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await ManagerStatesGroup.user.set()
        add_state(await state.get_state())
        ans, kb = get_user_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Открыть разрешения пользователя
@dp.callback_query_handler(CallbackData('user', 'id', 'action').filter(), state=ManagerStatesGroup.user)
async def user(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2], user_id=callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    else:
        await ManagerStatesGroup.permissions.set()
        add_state(await state.get_state())
        ans, kb = get_permissions_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
    await callback.answer()


# Разрешения пользователя
@dp.callback_query_handler(CallbackData('permissions', 'id', 'action').filter(), state=ManagerStatesGroup.permissions)
async def user(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'back':
        await set_state()
        ans, kb = get_keyboard(STATES_LIST[-2], user_id=callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        delete_state()
    elif callback_data['action'] == 'delete_permission':
        db.delete_permission(user_id=callback_data['id'])
        ans, kb = get_permissions_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        await callback.answer('Разрешения успешно удалено!')
    else:
        db.add_permission(user_id=callback_data['id'])
        ans, kb = get_permissions_keyboard(callback_data['id'])
        await callback.message.edit_text(text=ans,
                                         reply_markup=kb)
        await callback.answer('Разрешения успешно добавлено!')
    await callback.answer()


# Ветка документов


# Ветка выхода

# Выйти из режима менеджера
@dp.callback_query_handler(text='exit', state=ManagerStatesGroup.start)
async def exit_manager(callback: types.CallbackQuery):
    delete_all_states()
    db.change_status_id(user_id=callback.from_user.id, status_id=1)
    await callback.answer('Вы успешно вышли!')
    await callback.message.delete()
    await callback.answer()
