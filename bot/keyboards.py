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


# USER

# Клавиатура команды "start"
def get_user_start_keyboard():
    answer = 'Добро пожаловать в Phone Fix Bot!'
    start_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='🛠 Ремонт телефонов 📱', callback_data='repairs_catalog')],
        [InlineKeyboardButton(text='Аксессуары 📲', callback_data='accessories_catalog')],
        [InlineKeyboardButton(text='Заказы 📝', callback_data='orders')],
        [InlineKeyboardButton(text='Поиск 🔍', callback_data='search')],
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
    answer = f'Аксессуар: {accessory[2]}\nОписание: {accessory[3]}\nХарактеристики: {accessory[4]}\nЦена: {accessory[5]}'
    accessory_keyboard = InlineKeyboardMarkup(row_width=1)
    if db.is_accessory_in_user(user_id=user_id, accessory_id=accessory_id):
        accessory_keyboard.add(InlineKeyboardButton(text='Убрать из желаемого', callback_data=cb.new(id=accessory[0], action='delete_desired')))
    else:
        accessory_keyboard.add(InlineKeyboardButton(text='Добавить в желаемое', callback_data=cb.new(id=accessory[0], action='add_desired')))
    accessory_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, accessory_keyboard, accessory[6]


# Ветка заказов

# Ветка поиска

# Ветка о нас


# MANAGER

def get_manager_start_keyboard():
    answer = 'Менеджер! Добро пожаловать в Phone Fix Bot!'
    start_manager_ikm = InlineKeyboardMarkup(inline_keyboard=[
    ])
    return answer, start_manager_ikm
