import sqlite3 as sq


# Класс базы данных
class DataBase:

    # Создание подлючения и курсора
    def __init__(self):
        self.conn = sq.connect('bot/db/database.db')
        self.cursor = self.conn.cursor()

    # Вернуть данные
    def get_data(self, **kwargs):
        if 'where' in kwargs:
            self.cursor.execute(f'SELECT * FROM {kwargs["table"]} WHERE {kwargs["op1"]} = "{kwargs["op2"]}"')
        else:
            self.cursor.execute(f"SELECT * FROM {kwargs['table']}")
        return self.cursor.fetchall()

    # Поменять status_id у пользователя
    def change_status_id(self, **kwargs):
        self.cursor.execute(f'UPDATE users SET status_id = {kwargs["status_id"]} WHERE id = {kwargs["user_id"]}')
        self.conn.commit()

    # USER

    # Проверка существования user-а в бд
    def check_user(self, **kwargs):
        self.cursor.execute('SELECT * FROM users')
        users = self.cursor.fetchall()
        if not users:
            self.cursor.execute(f'INSERT INTO users(id, user_name, fl_name) VALUES ({kwargs["user_id"]}, "{kwargs["user_name"]}", "{kwargs["fl_name"]}")')
            self.conn.commit()
        else:
            self.cursor.execute(f'SELECT * FROM users WHERE id = {kwargs["user_id"]}')
            user = self.cursor.fetchall()
            if not user:
                self.cursor.execute(
                    f'INSERT INTO users(id, user_name, fl_name) VALUES ({kwargs["user_id"]}, "{kwargs["user_name"]}", "{kwargs["fl_name"]}")')
                self.conn.commit()

    # Вернуть статус user-а
    def get_status_id(self, **kwargs):
        self.cursor.execute(f'SELECT status_id FROM users WHERE id = {kwargs["user_id"]}')
        status_id = self.cursor.fetchall()[0][0]
        return status_id

    # Ветка ремонта

    # Добавить запись в заказы услуг
    def insert_orders_repair(self, **kwargs):
        self.cursor.execute(f'SELECT * FROM orders_repair WHERE user_id = {kwargs["user_id"]}')
        user_notes = self.cursor.fetchall()
        if len(user_notes) < 3:
            self.cursor.execute(
                f'INSERT INTO orders_repair(user_id, repair_id, model_id) VALUES ({kwargs["user_id"]}, {kwargs["repair_id"]}, {kwargs["model_id"]})')
            self.conn.commit()
            return 'Заказ оформлен!'
        else:
            return 'Нельзя заказывать больше трёх услуг!'

    # Ветка аксессуаров

    # Вернуть аксессуары в зависимости от сортировки
    def get_accessories(self, **kwargs):
        self.cursor.execute(
            f'SELECT * FROM accessories WHERE catalog_id = {kwargs["catalog_id"]} ' + kwargs['order_by'])
        accessories = self.cursor.fetchall()
        return accessories

    # Добавление/удаление желаемого пользователя
    def insert_on_delete_desired(self, **kwargs):
        if kwargs['action'] == 'add_desired':
            self.cursor.execute(
                f'INSERT INTO desired(user_id, accessory_id) VALUES ({kwargs["user_id"]}, {kwargs["accessory_id"]})')
        else:
            self.cursor.execute(
                f'DELETE FROM desired WHERE user_id = {kwargs["user_id"]} AND accessory_id = {kwargs["accessory_id"]}')
        self.conn.commit()

    # Проверка на наличие желаемого у пользователя
    def is_accessory_in_user(self, **kwargs):
        self.cursor.execute(
            f'SELECT * FROM desired WHERE user_id = {kwargs["user_id"]} AND accessory_id = {kwargs["accessory_id"]}')
        if self.cursor.fetchall():
            return True
        else:
            return False

    # Ветка заказов

    # Отмена заказа услуг ремонта
    def cancel_order_repair(self, **kwargs):
        self.cursor.execute(f'DELETE FROM orders_repair WHERE id = {kwargs["order_id"]}')
        self.conn.commit()

    # Ветка поиска

    # Нахождение услуг ремонта по наименованию
    def get_found_repairs_data(self, **kwargs):
        self.cursor.execute(f'SELECT * FROM repairs_catalog WHERE `name_lc` LIKE "%{kwargs["search_query"].lower()}%"')
        found_answers = self.cursor.fetchall()
        return found_answers

    # Нахождение аксессуаров по наименованию
    def get_found_accessories_data(self, **kwargs):
        self.cursor.execute(f'SELECT * FROM accessories WHERE `name_lc` LIKE "%{kwargs["search_query"].lower()}%"')
        found_answers = self.cursor.fetchall()
        return found_answers

    # MANAGER

    # Ветка услуг ремонта

    # Добавление услуги ремонта
    def add_repair(self, **kwargs):
        self.cursor.execute(
            f'INSERT INTO repairs_catalog(name, description, cost, name_lc) VALUES ("{kwargs["name"]}", "{kwargs["description"]}", "{kwargs["cost"]}", "{kwargs["name"].lower()}")')
        self.conn.commit()

    # Удаление услуги на ремонт
    def delete_repair(self, **kwargs):
        self.cursor.execute(f'DELETE FROM repairs_catalog WHERE id = {kwargs["repair_id"]}')
        self.conn.commit()

    # Смена значения поля услуги ремонта
    def update_repair(self, **kwargs):
        if kwargs['field'] == 'name':
            self.cursor.execute(
                f'UPDATE repairs_catalog SET name = "{kwargs["new_value"]}", name_lc = "{kwargs["new_value"].lower()}" WHERE id = {kwargs["repair_id"]}')
        else:
            self.cursor.execute(
                f'UPDATE repairs_catalog SET {kwargs["field"]} = "{kwargs["new_value"]}" WHERE id = {kwargs["repair_id"]}')
        self.conn.commit()

    # Изменение состояния просмотра
    def change_is_processed(self, **kwargs):
        self.cursor.execute(f'SELECT is_processed FROM orders_repair WHERE id = {kwargs["order_repair_id"]}')
        is_processed = self.cursor.fetchall()[0][0]
        if is_processed == 0:
            self.cursor.execute(f'UPDATE orders_repair SET is_processed = 1 WHERE id = {kwargs["order_repair_id"]}')
            self.conn.commit()

    # Выполнение заказа на ремонт услуги
    def change_is_completed(self, **kwargs):
        self.cursor.execute(f'UPDATE orders_repair SET is_completed = 1 WHERE id = {kwargs["order_repair_id"]}')
        self.conn.commit()

    # Ветка аксессуаров

    # Добавление категории аксессуаров
    def add_accessory_catalog(self, **kwargs):
        self.cursor.execute(f'INSERT INTO accessories_catalog(name) VALUES ("{kwargs["name"]}")')
        self.conn.commit()

    # Удаление категории аксессуаров
    def delete_accessory_catalog(self, **kwargs):
        self.cursor.execute(f'DELETE FROM accessories_catalog WHERE id = {kwargs["accessory_catalog_id"]}')
        self.conn.commit()

    # Добавление аксессуара
    def add_accessory(self, **kwargs):
        self.cursor.execute(
            f'INSERT INTO accessories(catalog_id, name, description, specifications, cost, photo, name_lc) VALUES ({kwargs["catalog_id"]}, "{kwargs["name"]}", "{kwargs["description"]}", "{kwargs["specifications"]}", {kwargs["cost"]}, "{kwargs["photo"]}", "{kwargs["name"].lower()}")')
        self.conn.commit()

    # Удаление аксессуара
    def delete_accessory(self, **kwargs):
        self.cursor.execute(f'DELETE FROM accessories WHERE id = {kwargs["accessory_id"]}')
        self.conn.commit()

    # Смена значения поля аксессуара
    def update_accessory(self, **kwargs):
        if kwargs['field'] == 'name':
            self.cursor.execute(
                f'UPDATE accessories SET name = "{kwargs["new_value"]}", name_lc = "{kwargs["new_value"].lower()}" WHERE id = {kwargs["accessory_id"]}')
        else:
            self.cursor.execute(
                f'UPDATE accessories SET {kwargs["field"]} = "{kwargs["new_value"]}" WHERE id = {kwargs["accessory_id"]}')
        self.conn.commit()

    # Ветка пользователей

    # Вернуть разрешения пользователя
    def get_permissions_user(self, **kwargs):
        self.cursor.execute(f'SELECT * FROM permissions WHERE user_id = {kwargs["user_id"]}')
        permissions_user = self.cursor.fetchall()
        if permissions_user:
            return True
        else:
            return False

    # Удалить разрешение у пользователя
    def delete_permission(self, **kwargs):
        self.cursor.execute(f'DELETE FROM permissions WHERE user_id = {kwargs["user_id"]}')
        self.conn.commit()

    # Добавить разрешение пользователю
    def add_permission(self, **kwargs):
        self.cursor.execute(f'INSERT INTO permissions(user_id, status_id) VALUES ({kwargs["user_id"]}, 2)')
        self.conn.commit()


# Экземпляр базы данных
db = DataBase()
