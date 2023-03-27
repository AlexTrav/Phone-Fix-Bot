from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStatesGroup(StatesGroup):
    start = State()
    repair = State()
    accessories = State()
    orders = State()
    search = State()
    about = State()


class ManagerStatesGroup(StatesGroup):
    start = State()

