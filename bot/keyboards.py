from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_user_start_keyboard():
    start_ikm = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='🛠 Ремонт телефонов 📱', callback_data='repairs_catalog')],
        [InlineKeyboardButton(text='Аксессуары 📲', callback_data='accessories_catalog')],
        [InlineKeyboardButton(text='Заказы 📝', callback_data='orders')],
        [InlineKeyboardButton(text='Поиск 🔍', callback_data='search')],
        [InlineKeyboardButton(text='О нас 👤', callback_data='about')]
    ])
    return start_ikm


def get_manager_start_keyboard():
    start_manager_ikm = InlineKeyboardMarkup(inline_keyboard=[
    ])
    return start_manager_ikm
