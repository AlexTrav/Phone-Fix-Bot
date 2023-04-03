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

    # MANAGER


# Экземпляр базы данных
db = DataBase()
