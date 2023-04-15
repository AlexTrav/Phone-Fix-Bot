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
    select_search = State()

    search_repairs = State()
    found_repair = State()

    search_accessories = State()
    found_accessory = State()

    # Ветка о нас
    about_module = State()


# Класс состояний менеджера
class ManagerStatesGroup(StatesGroup):
    # Начало
    start = State()

    # Ветка услуг ремонта
    repairs_catalog = State()
    repair_item = State()

    orders_repair = State()
    order_repair = State()

    add_repair = State()
    update_repair = State()
    update_field_repair = State()

    # Ветка аксессуаров
    accessories_catalog = State()
    accessories = State()
    accessory = State()

    desired_accessories = State()
    desired_accessory = State()

    add_accessory_catalog = State()
    add_accessory = State()

    delete_accessory_catalog = State()

    update_accessory = State()
    update_field_accessory = State()

    # Ветка пользователей
    users = State()
    user = State()
    permissions = State()

    # Ветка документов
