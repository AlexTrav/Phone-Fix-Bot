from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from bot.db.database import db


# Кнопка назад

# Список последних состояний
STATES_LIST = []


# Добавить состояние
def add_state(state):
    STATES_LIST.append(state)


# Удалить состояние
def delete_state():
    STATES_LIST.pop(-1)


# Удалить все состояния
def delete_all_states():
    STATES_LIST.clear()


# Отправить клавиатуру в зависимости от состояния
def get_keyboard(state, **kwargs):

    # USER

    if state == 'UserStatesGroup:start':
        return get_user_start_keyboard()
    if state == 'UserStatesGroup:repair':
        return get_repairs_catalog_keyboard()
    if state == 'UserStatesGroup:repair_item':
        return get_repair_item_keyboard(kwargs['service_id'])
    if state == 'UserStatesGroup:to_order':
        return get_phone_models_category_keyboard()
    if state == 'UserStatesGroup:accessories_catalog':
        return get_accessories_catalog_keyboard()
    if state == 'UserStatesGroup:accessories':
        return get_accessories_keyboard(kwargs['catalog_id'])
    if state == 'UserStatesGroup:select_orders':
        return get_select_orders_keyboard()
    if state == 'UserStatesGroup:desired':
        return get_desired_keyboard(kwargs['user_id'])
    if state == 'UserStatesGroup:orders_repair':
        return get_orders_repair(kwargs['user_id'])
    if state == 'UserStatesGroup:select_search':
        return get_select_search_keyboard()
    if state == 'UserStatesGroup:search_repairs':
        return get_search_repairs_keyboard()
    if state == 'UserStatesGroup:search_accessories':
        return get_search_accessories_keyboard()
    if state == 'UserStatesGroup:found_repair':
        return get_repair_item_keyboard(kwargs['service_id'])

    # MANAGER


# USER

# Клавиатура команды "start"
def get_user_start_keyboard():
    answer = 'Добро пожаловать в Phone Fix Bot!'
    start_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='🛠 Ремонт телефонов 📱', callback_data='repairs_catalog')],
        [InlineKeyboardButton(text='Аксессуары 📲', callback_data='accessories_catalog')],
        [InlineKeyboardButton(text='Заказы 📝', callback_data='select_orders')],
        [InlineKeyboardButton(text='Поиск 🔍', callback_data='select_search')],
        [InlineKeyboardButton(text='О нас 👤', callback_data='about')]
    ])
    return answer, start_keyboard


# Ветка ремонта

# Клавиатура каталога услуг
def get_repairs_catalog_keyboard():
    cb = CallbackData('repairs_catalog', 'id', 'action')
    answer = 'Выберите категорию ремонта:'
    repairs_catalog_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    i = 0
    for category in db.get_data(table='repairs_catalog'):
        buttons.append(InlineKeyboardButton(text=category[1], callback_data=cb.new(id=category[0], action='category')))
        i += 1
    repairs_catalog_keyboard.add(*buttons).add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, repairs_catalog_keyboard


# Клавиатура услуги
def get_repair_item_keyboard(service_id):
    cb = CallbackData('repair_item', 'id', 'action')
    service = db.get_data(table='repairs_catalog', where=1, op1='id', op2=service_id)[0]
    answer = f'''Наименование услуги: {service[1]}; \nОписание услуги: {service[2]}; \nЦена услуги: {service[3]}₸.'''.lstrip(' ')
    repair_item_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Заказать 📝', callback_data=cb.new(id=service[0], action='order'))],
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back'))]
    ])
    return answer, repair_item_keyboard


# Клавиатура категории телеофонов
def get_phone_models_category_keyboard():
    cb = CallbackData('category_models', 'id', 'action')
    answer = 'Выберите брэнд телефона:'
    phone_models_category_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for category_model in db.get_data(table='phone_models_category'):
        buttons.append(InlineKeyboardButton(text=category_model[1], callback_data=cb.new(id=category_model[0], action='category')))
    phone_models_category_keyboard.add(*buttons).add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, phone_models_category_keyboard


# Клавиатура моделий телефона
def get_phone_models_keyboard(category_model_id):
    cb = CallbackData('models', 'id', 'action')
    answer = 'Выберите модель телефона:'
    phone_models_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for model in db.get_data(table='phone_models', where=1, op1='id', op2=category_model_id):
        buttons.append(InlineKeyboardButton(text=model[2], callback_data=cb.new(id=model[0], action='model')))
    phone_models_keyboard.add(*buttons).add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, phone_models_keyboard


# Ветка аксессуаров

# Клавиатура каталога аксессуаров
def get_accessories_catalog_keyboard():
    cb = CallbackData('accessories_catalog', 'id', 'action')
    answer = 'Выберите каталог аксессуаров:'
    accessories_catalog_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for catalog in db.get_data(table='accessories_catalog'):
        buttons.append(InlineKeyboardButton(text=catalog[1], callback_data=cb.new(id=catalog[0], action='catalog')))
    accessories_catalog_keyboard.add(*buttons).add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, accessories_catalog_keyboard


# Клавиатура выбора аксессуара
def get_accessories_keyboard(catalog_id):
    cb = CallbackData('accessories', 'id', 'action')
    answer = 'Выберите аксессуар:'
    accessories_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for accessory in db.get_data(table='accessories', where=1, op1='catalog_id', op2=catalog_id):
        buttons.append(InlineKeyboardButton(text=accessory[2], callback_data=cb.new(id=accessory[0], action='catalog')))
    accessories_keyboard.add(*buttons).add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, accessories_keyboard


# Клавиатура и описание аксессуара
def get_accessory_keyboard(accessory_id, user_id):
    cb = CallbackData('accessory', 'id', 'action')
    accessory = db.get_data(table='accessories', where=1, op1='id', op2=accessory_id)[0]
    answer = f'Аксессуар: {accessory[2]}\nОписание: {accessory[3]}\nХарактеристики: {accessory[4]}\nЦена: {accessory[5]}₸'
    accessory_keyboard = InlineKeyboardMarkup(row_width=1)
    if db.is_accessory_in_user(user_id=user_id, accessory_id=accessory_id):
        accessory_keyboard.add(InlineKeyboardButton(text='Убрать из желаемого', callback_data=cb.new(id=accessory[0], action='delete_desired')))
    else:
        accessory_keyboard.add(InlineKeyboardButton(text='Добавить в желаемое', callback_data=cb.new(id=accessory[0], action='add_desired')))
    accessory_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, accessory_keyboard, accessory[6]


# Ветка заказов

# Клавиатура выбора заказов
def get_select_orders_keyboard():
    cb = CallbackData('select_orders', 'action')
    answer = 'Выберите тип заказов:'
    select_orders_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='📝 Заказы услуг на ремонт 🛠', callback_data=cb.new(action='orders_repair'))],
        [InlineKeyboardButton(text='📝 Желаемое 📲', callback_data=cb.new(action='desired'))],
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, select_orders_keyboard


# Клавиатура желаемого user-а
def get_desired_keyboard(user_id):
    cb = CallbackData('desired', 'id', 'action')
    answer = 'Выберите желаемое:'
    desired_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for desire in db.get_data(table='desired', where=1, op1='user_id', op2=user_id):
        accessory = db.get_data(table='accessories', where=1, op1='id', op2=desire[2])[0]
        buttons.append(InlineKeyboardButton(text=accessory[2], callback_data=cb.new(id=accessory[0], action='catalog')))
    desired_keyboard.add(*buttons).add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, desired_keyboard


# Клавиатура заказов услуг на ремонт
def get_orders_repair(user_id):
    cb = CallbackData('orders_repair', 'id', 'action')
    answer = 'Выберите заказ на услугу:'
    orders_repair_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for order_repair in db.get_data(table='orders_repair', where=1, op1='user_id', op2=user_id):
        repair = db.get_data(table='repairs_catalog', where=1, op1='id', op2=order_repair[2])[0]
        buttons.append(InlineKeyboardButton(text=repair[1], callback_data=cb.new(id=order_repair[0], action='catalog')))
    orders_repair_keyboard.add(*buttons).add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, orders_repair_keyboard


# Клавиатура заказа услуг на ремонт
def get_order_repair(order_id):
    cb = CallbackData('order_repair', 'id', 'action')
    order_repair = db.get_data(table='orders_repair', where=1, op1='id', op2=order_id)[0]
    repair = db.get_data(table='repairs_catalog', where=1, op1='id', op2=order_repair[2])[0]
    model = db.get_data(table='phone_models', where=1, op1='id', op2=order_repair[3])[0]
    is_processed = ['Не просмотрен', 'Просмотрен'][order_repair[4]]
    is_completed = ['Не выполнен', 'Выполнен'][order_repair[5]]
    answer = f'Заказ под номером: {order_repair[0]}\nЗаказанная услуга: {repair[1]}\nНа модель: {model[2]}\nЦена услуги: {repair[3]}₸\nСтатус просмотра: {is_processed}\nСтатус выполнения: {is_completed}'
    order_repair_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Отменить', callback_data=cb.new(id=order_repair[0], action='cancel_order'))],
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back'))]
    ])
    return answer, order_repair_keyboard


# Ветка поиска

# Клавиатура выбора поиска
def get_select_search_keyboard():
    cb = CallbackData('select_search', 'action')
    answer = 'Выберите тип поиска:'
    select_search_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='🔍 Поиск услуги на ремонт 🛠', callback_data=cb.new(action='search_repair'))],
        [InlineKeyboardButton(text='🔍 Поиск аксессуара 📲', callback_data=cb.new(action='search_accessory'))],
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, select_search_keyboard


# Клавиатура поиска услуг ремонта
def get_search_repairs_keyboard():
    cb = CallbackData('search_repairs', 'action')
    answer = 'Введите название услуги ремонта следующим сообщением:'
    search_repairs_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, search_repairs_keyboard


# Клавиатура поиска аксессуаров
def get_search_accessories_keyboard():
    cb = CallbackData('search_accessories', 'action')
    answer = 'Введите название аксессуара следующим сообщением:'
    search_accessories_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, search_accessories_keyboard


# Клавиатура найденных услуг ремонта
def get_found_repairs_keyboard(search_query):
    cb = CallbackData('found_repairs', 'id', 'action')
    found_repairs = db.get_found_repairs_data(search_query=search_query)
    if len(found_repairs) > 0:
        answer = f'Найдено совпадений: {len(found_repairs)}'
        found_repairs_keyboard = InlineKeyboardMarkup(row_width=1)
        buttons = []
        for found_repair in found_repairs:
            buttons.append(InlineKeyboardButton(text=found_repair[1], callback_data=cb.new(id=found_repair[0], action='repair')))
        found_repairs_keyboard.add(*buttons).add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    else:
        answer = 'К сожалению совпадений не найдено'
        found_repairs_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back'))]
        ])
    return answer, found_repairs_keyboard


# Клавиатура найденных аксессуаров
def get_found_accessories_keyboard(search_query):
    cb = CallbackData('found_accessories', 'id', 'action')
    found_accessories = db.get_found_accessories_data(search_query=search_query)
    if len(found_accessories) > 0:
        answer = f'Найдено совпадений: {len(found_accessories)}'
        found_accessories_keyboard = InlineKeyboardMarkup(row_width=1)
        buttons = []
        for found_accessory in found_accessories:
            buttons.append(InlineKeyboardButton(text=found_accessory[2], callback_data=cb.new(id=found_accessory[0], action='repair')))
        found_accessories_keyboard.add(*buttons).add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    else:
        answer = 'К сожалению совпадений не найдено'
        found_accessories_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back'))]
        ])
    return answer, found_accessories_keyboard


# Ветка о нас

# Клавиатура модуля "О нас"
def get_about_keyboard():
    cb = CallbackData('about', 'action')
    answer = 'Телеграм бот создан в целях выполнения дипломного проекта.\nГлавный разработчик: Абдукодиров Даврон.'
    about_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Связь', url='https://t.me/abdukodiiirov')],
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, about_keyboard


# MANAGER

def get_manager_start_keyboard():
    answer = 'Менеджер! Добро пожаловать в Phone Fix Bot!'
    manager_start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    ])
    return answer, manager_start_keyboard
