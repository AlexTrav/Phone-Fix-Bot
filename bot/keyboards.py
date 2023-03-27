from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from bot.db.database import db


# USER

def get_user_start_keyboard():
    start_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='🛠 Ремонт телефонов 📱', callback_data='repairs_catalog')],
        [InlineKeyboardButton(text='Аксессуары 📲', callback_data='accessories_catalog')],
        [InlineKeyboardButton(text='Заказы 📝', callback_data='orders')],
        [InlineKeyboardButton(text='Поиск 🔍', callback_data='search')],
        [InlineKeyboardButton(text='О нас 👤', callback_data='about')]
    ])
    return start_keyboard


# Ветка ремонта

def get_repairs_catalog_keyboard():
    cb = CallbackData('repairs_catalog', 'id', 'action')
    repairs_catalog_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    i = 0
    for category in db.get_data(table='repairs_catalog'):
        buttons.append(InlineKeyboardButton(text=category[1], callback_data=cb.new(id=category[0], action='category')))
        i += 1
    repairs_catalog_keyboard.add(*buttons).add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return repairs_catalog_keyboard


# Ветка аксессуаров

# Ветка заказов

# Ветка поиска

# Ветка о нас


# MANAGER

def get_manager_start_keyboard():
    start_manager_ikm = InlineKeyboardMarkup(inline_keyboard=[
    ])
    return start_manager_ikm
