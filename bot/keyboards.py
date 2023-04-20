from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from bot.db.database import db


# Кнопка назад

# Список последних состояний
STATES_LIST = []
# Переменная для сотртировки
SORTING = ''


# Добавить состояние
def add_state(state):
    STATES_LIST.append(state)


# Удалить состояние
def delete_state():
    STATES_LIST.pop(-1)


# Удалить все состояния
def delete_all_states():
    if not STATES_LIST:
        STATES_LIST.clear()


# Отправить клавиатуру в зависимости от состояния
def get_keyboard(state, **kwargs):

    # USER
    if state == 'UserStatesGroup:start':
        return get_user_start_keyboard(kwargs['user_id'])
    # Ветка услуг ремонта
    if state == 'UserStatesGroup:repair':
        return get_repairs_catalog_keyboard()
    if state == 'UserStatesGroup:repair_item':
        return get_repair_item_keyboard(kwargs['service_id'])
    if state == 'UserStatesGroup:to_order':
        return get_phone_models_category_keyboard()
    # Ветка аксессуаров
    if state == 'UserStatesGroup:accessories_catalog':
        return get_accessories_catalog_keyboard()
    if state == 'UserStatesGroup:accessories':
        return get_accessories_keyboard(kwargs['catalog_id'])
    # Ветка заказов
    if state == 'UserStatesGroup:select_orders':
        return get_select_orders_keyboard()
    if state == 'UserStatesGroup:desired':
        return get_desired_keyboard(kwargs['user_id'])
    if state == 'UserStatesGroup:orders_repair':
        return get_orders_repair_keyboard(kwargs['user_id'])
    # Ветка поиска
    if state == 'UserStatesGroup:select_search':
        return get_select_search_keyboard()
    if state == 'UserStatesGroup:search_repairs':
        return get_search_repairs_keyboard()
    if state == 'UserStatesGroup:search_accessories':
        return get_search_accessories_keyboard()
    if state == 'UserStatesGroup:found_repair':
        return get_repair_item_keyboard(kwargs['service_id'])

    # MANAGER
    if state == 'ManagerStatesGroup:start':
        return get_manager_start_keyboard()
    # Ветка услуг ремонта
    if state == 'ManagerStatesGroup:repairs_catalog':
        return get_repairs_catalog_manager_keyboard()
    if state == 'ManagerStatesGroup:repair_item':
        return get_repair_item_manager_keyboard(kwargs['repair_id'])
    if state == 'ManagerStatesGroup:update_repair':
        return get_update_repair_keyboard()
    if state == 'ManagerStatesGroup:orders_repair':
        return get_orders_repair_manager_keyboard()
    # Ветка аксессуаров
    if state == 'ManagerStatesGroup:accessories_catalog':
        return get_accessories_catalog_manager_keyboard()
    if state == 'ManagerStatesGroup:accessories':
        return get_accessories_manager_keyboard(kwargs['category_id'])
    if state == 'ManagerStatesGroup:accessory':
        return get_accessory_manager_keyboard(kwargs['accessory_id'])
    if state == 'ManagerStatesGroup:update_accessory':
        return get_update_accessory_keyboard()
    if state == 'ManagerStatesGroup:desired_accessories':
        return get_desired_manager_keyboard()

    # Ветка пользователей
    if state == 'ManagerStatesGroup:users':
        return get_users_keyboard()
    if state == 'ManagerStatesGroup:user':
        return get_user_keyboard(kwargs['user_id'])
    # Ветка документов
    if state == 'ManagerStatesGroup:documents':
        return get_documents_keyboard()


# USER

# Клавиатура команды "start"
def get_user_start_keyboard(user_id):
    answer = 'Добро пожаловать в Phone Fix Bot!'
    start_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='🛠 Ремонт телефонов 📱', callback_data='repairs_catalog')],
        [InlineKeyboardButton(text='Аксессуары 📲', callback_data='accessories_catalog')],
        [InlineKeyboardButton(text='Заказы 📝', callback_data='select_orders')],
        [InlineKeyboardButton(text='Поиск 🔍', callback_data='select_search')],
        [InlineKeyboardButton(text='О нас 👤', callback_data='about')]
    ])
    if user_id in get_permissions_id():
        start_keyboard.add(InlineKeyboardButton(text='Войти как менеджер 🧑‍💻', callback_data='login_manager'))
    return answer, start_keyboard


# Вернуть список ключей сотрудников
def get_permissions_id():
    permissions_id = []
    for permission in db.get_data(table='permissions'):
        permissions_id.append(permission[0])
    return permissions_id


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
    for model in db.get_data(table='phone_models', where=1, op1='category_id', op2=category_model_id):
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
        accessories = db.get_data(table='accessories', where=1, op1='catalog_id', op2=catalog[0])
        if accessories:
            buttons.append(InlineKeyboardButton(text=catalog[1], callback_data=cb.new(id=catalog[0], action='catalog')))
    accessories_catalog_keyboard.add(*buttons).add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, accessories_catalog_keyboard


# Клавиатура выбора аксессуара
def get_accessories_keyboard(catalog_id):
    cb = CallbackData('accessories', 'id', 'action')
    answer = 'Выберите аксессуар:'
    accessories_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    accessories = db.get_accessories(catalog_id=catalog_id, order_by=SORTING)
    for accessory in accessories:
        buttons.append(InlineKeyboardButton(text=accessory[2], callback_data=cb.new(id=accessory[0], action='catalog')))
    accessories_keyboard.add(*buttons)
    if len(accessories) > 1:
        accessories_keyboard.add(InlineKeyboardButton(text='📋 Отсортировать по умолчанию 📋', callback_data=cb.new(id=-1, action='sort_default')))
        accessories_keyboard.add(InlineKeyboardButton(text='⬆️ Отсортировать по возрастанию цены 💵', callback_data=cb.new(id=-1, action='sort_asc')))
        accessories_keyboard.add(InlineKeyboardButton(text='⬇️ Отсортировать по убыванию цены 💵', callback_data=cb.new(id=-1, action='sort_desc')))
    accessories_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, accessories_keyboard


# Установка сортировки
def set_sorting_answer(action):
    global SORTING
    if action == 'sort_default':
        if SORTING == '':
            answer = 'Сортировка по умолчанию уже выбрана!'
        else:
            SORTING = ''
            answer = 'Выбрана сортировка по умолчанию'
    elif action == 'sort_asc':
        if SORTING == 'ORDER BY cost ASC':
            answer = 'Сортировка по возрастанию цены уже выбрана!'
        else:
            SORTING = 'ORDER BY cost ASC'
            answer = 'Выбрана сортировка по возрастанию'
    else:
        if SORTING == 'ORDER BY cost DESC':
            answer = 'Сортировка по убыванию цены уже выбрана!'
        else:
            SORTING = 'ORDER BY cost DESC'
            answer = 'Выбрана сортировка по убыванию цены'
    return answer


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
def get_orders_repair_keyboard(user_id):
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
def get_order_repair_keyboard(order_id):
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

# Клавиатура команды start
def get_manager_start_keyboard():
    answer = 'Менеджер! Добро пожаловать в Phone Fix Bot!'
    manager_start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Услуги ремонта 🛠', callback_data='repairs_catalog')],
        [InlineKeyboardButton(text='Аксессуары 📲', callback_data='accessories_catalog')],
        [InlineKeyboardButton(text='Пользователи 👤', callback_data='users')],
        [InlineKeyboardButton(text='Документы 📑', callback_data='documents')],
        [InlineKeyboardButton(text='Выйти 🚪', callback_data='exit')]
    ])
    return answer, manager_start_keyboard


# Ветка услуг ремонта

# Клавиатура услуг ремонта manager-а
def get_repairs_catalog_manager_keyboard():
    cb = CallbackData('repairs_catalog', 'id', 'action')
    answer = 'Каталог услуг на ремонт\nВыберите действие:'
    repairs_catalog_keyboard = InlineKeyboardMarkup()
    for repair in db.get_data(table='repairs_catalog'):
        repairs_catalog_keyboard.add(InlineKeyboardButton(text=repair[1], callback_data=cb.new(id=repair[0], action='category')))
    repairs_catalog_keyboard.add(InlineKeyboardButton(text='Заказанные услуги ⚙️', callback_data=cb.new(id=-3, action='orders_repair')), InlineKeyboardButton(text='Добавить услугу ремонта ➕', callback_data=cb.new(id=-2, action='add')))
    repairs_catalog_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, repairs_catalog_keyboard


# Клавиатура услуги ремонта manager-а
def get_repair_item_manager_keyboard(repair_id):
    cb = CallbackData('repair_item', 'id', 'action')
    repair = db.get_data(table='repairs_catalog', where=1, op1='id', op2=repair_id)[0]
    answer = f'''Наименование услуги: {repair[1]}; \nОписание услуги: {repair[2]}; \nЦена услуги: {repair[3]}₸.'''.lstrip(' ')
    repair_item_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Редактировать ✏️', callback_data=cb.new(id=repair[0], action='update'))],
        [InlineKeyboardButton(text='Удалить ✖️', callback_data=cb.new(id=repair[0], action='delete'))],
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back'))]
    ])
    return answer, repair_item_keyboard


# Клавиатура добавление услуги ремонта
def get_add_repair_item_keyboard():
    cb = CallbackData('repair_item', 'action')
    answer = 'Добавление услуги на ремонт\nВведите наименование; описание; цену следующим сообщением:\nКаждый параметр с новой строки, всего 3 параметра'
    add_repair_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, add_repair_keyboard


# Клавиатура выбора поля на редактирование услуги ремонта
def get_update_repair_keyboard():
    cb = CallbackData('update_repair', 'action')
    answer = 'Выберите поле для редактирования услуги ремонта'
    update_repair_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Наименование', callback_data=cb.new(action='name'))],
        [InlineKeyboardButton(text='Описание', callback_data=cb.new(action='description'))],
        [InlineKeyboardButton(text='Цена', callback_data=cb.new(action='cost'))],
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, update_repair_keyboard


# Клавиатура смены значения поля услуги ремонта
def get_update_field_repair_keyboard(action):
    cb = CallbackData('update_field_repair', 'action')
    answer = f'Введите новое значение для поля "{action}", следующим сообщением:'
    update_field_repair_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, update_field_repair_keyboard


# Клавиатура заказанных услуг ремонта
def get_orders_repair_manager_keyboard():
    cb = CallbackData('orders_repair', 'id', 'action')
    answer = f'Выберите заказанную услугу:'
    orders_repair_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for order_repair in db.get_data(table='orders_repair'):
        repair = db.get_data(table='repairs_catalog', where=1, op1='id', op2=order_repair[2])[0]
        is_processed = [' [Не просмотрен;', ' [Просмотрен;'][order_repair[4]]
        is_completed = [' Не выполнен] ', ' Выполнен] '][order_repair[5]]
        buttons.append(InlineKeyboardButton(text=repair[1] + is_processed + is_completed, callback_data=cb.new(id=order_repair[0], action='order_repair')))
    orders_repair_keyboard.add(*buttons).add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, orders_repair_keyboard


# Клавиатура заказа услуг на ремонт
def get_order_repair_manager_keyboard(order_id):
    cb = CallbackData('order_repair', 'id', 'action')
    order_repair = db.get_data(table='orders_repair', where=1, op1='id', op2=order_id)[0]
    repair = db.get_data(table='repairs_catalog', where=1, op1='id', op2=order_repair[2])[0]
    model = db.get_data(table='phone_models', where=1, op1='id', op2=order_repair[3])[0]
    is_processed = ['Не просмотрен', 'Просмотрен'][order_repair[4]]
    is_completed = ['Не выполнен', 'Выполнен'][order_repair[5]]
    answer = f'Заказ под номером: {order_repair[0]}\nЗаказан пользователем: {order_repair[1]}\nЗаказанная услуга: {repair[1]}\nНа модель: {model[2]}\nЦена услуги: {repair[3][1:]}₸\nСтатус просмотра: {is_processed}\nСтатус выполнения: {is_completed}'
    if order_repair[5] == 0:
        order_repair_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [InlineKeyboardButton(text='Выполнить', callback_data=cb.new(id=order_repair[0], action='execute'))],
            [InlineKeyboardButton(text='Отменить', callback_data=cb.new(id=order_repair[0], action='cancel_order'))],
            [InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back'))]
        ])
    else:
        order_repair_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [InlineKeyboardButton(text='Отменить', callback_data=cb.new(id=order_repair[0], action='cancel_order'))],
            [InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back'))]
        ])
    return answer, order_repair_keyboard


# Ветка аксессуаров

# Клавиатура выбора каталога аксессуаров
def get_accessories_catalog_manager_keyboard():
    cb = CallbackData('accessories_catalog', 'id', 'action')
    answer = 'Выберите каталог аксессуаров:'
    accessories_catalog_keyboard = InlineKeyboardMarkup()
    for catalog in db.get_data(table='accessories_catalog'):
        accessories_catalog_keyboard.add(InlineKeyboardButton(text=catalog[1], callback_data=cb.new(id=catalog[0], action='catalog')))
    accessories_catalog_keyboard.add(InlineKeyboardButton(text='Желаемые акксесуары 📒', callback_data=cb.new(id=-2, action='desired')), InlineKeyboardButton(text='Добавить категорию ➕', callback_data=cb.new(id=-2, action='add')))
    accessories_catalog_keyboard.add(InlineKeyboardButton(text='Удалить каталог ✖️', callback_data=cb.new(id=-3, action='delete')))
    accessories_catalog_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, accessories_catalog_keyboard


# Клавиатура добавления категории аксессуаров
def get_add_accessory_catalog_keyboard():
    cb = CallbackData('add_accessory_catalog', 'action')
    answer = 'Добавление категории аксессуаров\nВведите "Наименование" новой категории следующим сообщением:\n'
    add_accessory_catalog = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, add_accessory_catalog


# Клавиатура удаления категории аксессуаров
def get_delete_accessory_catalog_keyboard():
    cb = CallbackData('delete_accessory_catalog', 'id', 'action')
    answer = 'Выберите каталог на удаление:'
    accessories_catalog_keyboard = InlineKeyboardMarkup()
    for catalog in db.get_data(table='accessories_catalog'):
        accessories_catalog_keyboard.add(InlineKeyboardButton(text=catalog[1], callback_data=cb.new(id=catalog[0], action='catalog')))
    accessories_catalog_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, accessories_catalog_keyboard


# Клавиатура выбора аксессуара
def get_accessories_manager_keyboard(catalog_id):
    cb = CallbackData('accessories', 'id', 'action')
    answer = 'Выберите аксессуар:'
    accessories_keyboard = InlineKeyboardMarkup(row_width=1)
    for accessory in db.get_accessories(catalog_id=catalog_id, order_by=SORTING):
        accessories_keyboard.add(InlineKeyboardButton(text=accessory[2], callback_data=cb.new(id=accessory[0], action='catalog')))
    accessories_keyboard.add(InlineKeyboardButton(text='Добавить аксессуар ➕', callback_data=cb.new(id=-2, action='add')))
    accessories_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, accessories_keyboard


# Клавиатура аксессуара
def get_accessory_manager_keyboard(accessory_id):
    cb = CallbackData('accessory', 'id', 'action')
    accessory = db.get_data(table='accessories', where=1, op1='id', op2=accessory_id)[0]
    answer = f'Аксессуар: {accessory[2]}\nОписание: {accessory[3]}\nХарактеристики: {accessory[4]}\nЦена: {accessory[5]}₸'
    accessory_keyboard = InlineKeyboardMarkup(row_width=1)
    accessory_keyboard.add(InlineKeyboardButton(text='Редактировать аксессуар ✏️', callback_data=cb.new(id=accessory[0], action='update')))
    accessory_keyboard.add(InlineKeyboardButton(text='Удалить аксессуар ✖️', callback_data=cb.new(id=accessory[0], action='delete')))
    accessory_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, accessory_keyboard, accessory[6]


# Клавиатура добавления аксессуара
def get_add_accessory_keyboard():
    cb = CallbackData('add_accessory', 'action')
    answer = 'Добавление аксеcсуара\nВведите наименование; описание; характеристики; цену; фото(ссылкой) следующим сообщением:\nКаждый параметр с новой строки, всего 5 параметров'
    add_accessory = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, add_accessory


# Клавиатура желаемых аксессуаров
def get_desired_manager_keyboard():
    cb = CallbackData('desired_accessories', 'id', 'action')
    answer = 'Самые желаемые аксессуары:'
    desired_accessories_keyboard = InlineKeyboardMarkup(row_width=1)
    most_desired_accessories = set()
    for desired_accessory in db.get_data(table='desired'):
        most_desired_accessories.add(desired_accessory[2])
    for accessory_id in most_desired_accessories:
        accessory = db.get_data(table='accessories', where=1, op1='id', op2=accessory_id)[0]
        desired_accessories_keyboard.add(InlineKeyboardButton(text=accessory[2], callback_data=cb.new(id=accessory[0], action='desired_accessory')))
    desired_accessories_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, desired_accessories_keyboard


# Клавиатура желаемого аксессуара
def get_desired_accessory_manager_keyboard(accessory_id):
    cb = CallbackData('desired_accessory', 'action')
    accessory = db.get_data(table='accessories', where=1, op1='id', op2=accessory_id)[0]
    answer = f'Аксессуар: {accessory[2]}\nОписание: {accessory[3]}\nХарактеристики: {accessory[4]}\nЦена: {accessory[5]}₸'
    accessory_keyboard = InlineKeyboardMarkup(row_width=1)
    accessory_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back')))
    return answer, accessory_keyboard, accessory[6]


# Клавиатура выбора поля для редактирования аксессуара
def get_update_accessory_keyboard():
    cb = CallbackData('update_accessory', 'action')
    answer = 'Выберите поле для редактирования аксессуара'
    update_accessory_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Наименование', callback_data=cb.new(action='name'))],
        [InlineKeyboardButton(text='Описание', callback_data=cb.new(action='description'))],
        [InlineKeyboardButton(text='Характеристики', callback_data=cb.new(action='specifications'))],
        [InlineKeyboardButton(text='Цена', callback_data=cb.new(action='cost'))],
        [InlineKeyboardButton(text='Фото', callback_data=cb.new(action='photo'))],
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, update_accessory_keyboard


# Клавиатура смены значения поля аксессуара
def get_update_field_accessory_keyboard(action):
    cb = CallbackData('update_field_accessory', 'action')
    answer = f'Введите новое значение для поля "{action}", следующим сообщением:'
    update_field_repair_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, update_field_repair_keyboard


# Ветка пользователей

# Клавиатура пользователей
def get_users_keyboard():
    cb = CallbackData('users', 'id', 'action')
    answer = 'Выберите пользователя:'
    users_keyboard = InlineKeyboardMarkup(row_width=1)
    for user in db.get_data(table='users'):
        users_keyboard.add(InlineKeyboardButton(text=user[2], callback_data=cb.new(id=user[0], action='user')))
    users_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, users_keyboard


# Клавиатура пользователя
def get_user_keyboard(user_id):
    cb = CallbackData('user', 'id', 'action')
    user = db.get_data(table='users', where=1, op1='id', op2=user_id)[0]
    link = f'https://t.me/{user[1]}'
    status = ['', 'Пользователь', 'Менеджер'][user[3]]
    answer = f'Пользователь: {user[0]};\nИмя: {user[2]};\n@Username: {user[1]};\nСсылка на пользователя: {link};\nСтатус входа: {status}.'
    user_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='Разрешения пользователя ✔️', callback_data=cb.new(id=user[0], action='permissions'))],
        [InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=user[0], action='back'))]
    ])
    return answer, user_keyboard


# Клавиатура разрешений пользователя
def get_permissions_keyboard(user_id):
    cb = CallbackData('permissions', 'id', 'action')
    permissions_keyboard = InlineKeyboardMarkup(row_width=1)
    answer = f'Пользователь: {user_id}\n'
    if db.get_permissions_user(user_id=user_id):
        answer += 'Имеет права: Менеджера'
        permissions_keyboard.add(InlineKeyboardButton(text='Отозвать права', callback_data=cb.new(id=user_id, action='delete_permission')))
    else:
        permissions_keyboard.add(InlineKeyboardButton(text='Выдать права менеджера', callback_data=cb.new(id=user_id, action='insert_permission')))
    permissions_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=user_id, action='back')))
    return answer, permissions_keyboard


# Ветка документов

# Клавиатура документов (выполненных услуг ремонта)
def get_documents_keyboard():
    cb = CallbackData('documents', 'id', 'action')
    answer = 'Документы по выполненным услугам ремонта\nВыберите документ:'
    documents_keyboard = InlineKeyboardMarkup(row_width=1)
    for document in db.get_data(table='orders_repair', where=1, op1='is_completed', op2=1):
        repair = db.get_data(table='repairs_catalog', where=1, op1='id', op2=document[2])[0]
        documents_keyboard.add(InlineKeyboardButton(text=repair[1], callback_data=cb.new(id=document[0], action='document')))
    documents_keyboard.add(InlineKeyboardButton(text='⬅️', callback_data=cb.new(id=-1, action='back')))
    return answer, documents_keyboard


# Клавиатура документа
def get_document_keyboard(document_id):
    cb = CallbackData('document', 'action')
    document = db.get_data(table='orders_repair', where=1, op1='id', op2=document_id)[0]
    repair = db.get_data(table='repairs_catalog', where=1, op1='id', op2=document[2])[0]
    model = db.get_data(table='phone_models', where=1, op1='id', op2=document[3])[0]
    answer = f'Документ под номером: {document[0]}\nУслуга заказана пользователем: {document[1]}\nЗаказанная услуга: {repair[1]}\nНа модель: {model[2]}\nОбщая стоимость заказа: {repair[3][1:]}₸'
    document_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
          [InlineKeyboardButton(text='⬅️', callback_data=cb.new(action='back'))]
    ])
    return answer, document_keyboard
