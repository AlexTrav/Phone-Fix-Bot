from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from bot.db.database import db


# Кнопка назад

STATES_LIST = []


def add_state(state):
    STATES_LIST.append(state)


def get_keyboard(state):
    if state == 'UserStatesGroup:start':
        return get_user_start_keyboard()
    if state == 'UserStatesGroup:repair':
        return get_repairs_catalog_keyboard()


# USER

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


def get_repair_item_keyboard(service_id):
    cb = CallbackData('repair_item', 'id', 'action')
    service = db.get_data(table='repairs_catalog', where=1, op1='id', op2=service_id)[0]
    answer = f'''Наименование услуги: {service[1]}; \nОписание услуги: {service[2]}; \nЦена услуги: {service[3]}₸.'''.lstrip(' ')
    repair_item_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Заказать 📝', callback_data=cb.new(id=service[0], action='order'))],
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back'))]
    ])
    return answer, repair_item_keyboard


# Ветка аксессуаров

# Ветка заказов

# Ветка поиска

# Ветка о нас


# MANAGER

def get_manager_start_keyboard():
    answer = 'Менеджер! Добро пожаловать в Phone Fix Bot!'
    start_manager_ikm = InlineKeyboardMarkup(inline_keyboard=[
    ])
    return answer, start_manager_ikm
