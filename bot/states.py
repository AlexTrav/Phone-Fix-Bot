from aiogram.dispatcher.filters.state import StatesGroup, State


# Класс состояний пользователя
class UserStatesGroup(StatesGroup):
    # Начало
    start = State()

    # Ветка ремонта
    repair = State()
    repair_item = State()
    to_order = State()

    # Ветка аксессуаров
    accessories_catalog = State()
    accessories = State()
    accessory = State()

    # Ветка заказов
    select_orders = State()

    desired = State()
    desire = State()

    orders_repair = State()
    order_repair = State()

    # Ветка поиска
    search = State()

    # Ветка о нас
    about = State()


# Класс состояний менеджера
class ManagerStatesGroup(StatesGroup):
    start = State()

