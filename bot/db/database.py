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
            self.cursor.execute(
                f'INSERT INTO users(id, user_name, fl_name) VALUES ({kwargs["user_id"]}, "{kwargs["user_name"]}", "{kwargs["fl_name"]}")')
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
            self.cursor.execute(f'INSERT INTO orders_repair(user_id, repair_id, model_id) VALUES ({kwargs["user_id"]}, {kwargs["repair_id"]}, {kwargs["model_id"]})')
            self.conn.commit()
            return 'Заказ оформлен!'
        else:
            return 'Нельзя заказывать больше трёх услуг!'

    # Ветка аксессуаров

    def get_accessories(self, **kwargs):
        self.cursor.execute(f'SELECT * FROM accessories WHERE catalog_id = {kwargs["catalog_id"]} ' + kwargs['order_by'])
        accessories = self.cursor.fetchall()
        return accessories

    # Добавление/удаление желаемого пользователя
    def insert_on_delete_desired(self, **kwargs):
        if kwargs['action'] == 'add_desired':
            self.cursor.execute(f'INSERT INTO desired(user_id, accessory_id) VALUES ({kwargs["user_id"]}, {kwargs["accessory_id"]})')
        else:
            self.cursor.execute(f'DELETE FROM desired WHERE user_id = {kwargs["user_id"]} AND accessory_id = {kwargs["accessory_id"]}')
        self.conn.commit()

    # Проверка на наличие желаемого у пользователя
    def is_accessory_in_user(self, **kwargs):
        self.cursor.execute(f'SELECT * FROM desired WHERE user_id = {kwargs["user_id"]} AND accessory_id = {kwargs["accessory_id"]}')
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
        self.cursor.execute(f'INSERT INTO repairs_catalog(name, description, cost, name_lc) VALUES ("{kwargs["name"]}", "{kwargs["description"]}", "{kwargs["cost"]}", "{kwargs["name"].lower()}")')
        self.conn.commit()

    # Удаление услуги на ремонт
    def delete_repair(self, **kwargs):
        self.cursor.execute(f'DELETE FROM repairs_catalog WHERE id = {kwargs["repair_id"]}')
        self.conn.commit()

    # Смена значения поля услуги ремонта
    def update_repair(self, **kwargs):
        if kwargs['field'] == 'name':
            self.cursor.execute(f'UPDATE repairs_catalog SET name = "{kwargs["new_value"]}", name_lc = "{kwargs["new_value"].lower()}" WHERE id = {kwargs["repair_id"]}')
        else:
            self.cursor.execute(f'UPDATE repairs_catalog SET {kwargs["field"]} = "{kwargs["new_value"]}" WHERE id = {kwargs["repair_id"]}')
        self.conn.commit()

    # Ветка аксессуаров

    # Ветка пользователей

    # Ветка документов


# Экземпляр базы данных
db = DataBase()
