from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStatesGroup(StatesGroup):
    start = State()


class ManagerStatesGroup(StatesGroup):
    start = State()
