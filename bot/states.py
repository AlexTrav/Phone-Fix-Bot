from aiogram.dispatcher.filters.state import StatesGroup, State


# Класс состояний пользователя
class UserStatesGroup(StatesGroup):
    start = State()
    repair = State()
    repair_item = State()
    accessories_catalog = State()
    accessories = State()
    accessory = State()
    to_order = State()
    orders = State()
    search = State()
    about = State()


# Класс состояний менеджера
class ManagerStatesGroup(StatesGroup):
    start = State()

