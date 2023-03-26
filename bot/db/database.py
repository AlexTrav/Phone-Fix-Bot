import sqlite3 as sq


class DataBase:

    def __init__(self):
        self.conn = sq.connect('bot/db/database.db')
        self.cursor = self.conn.cursor()

    def get_data(self, **kwargs):
        if 'where' in kwargs:
            self.cursor.execute(f'SELECT * FROM {kwargs["table"]} WHERE {kwargs["op1"]} = "{kwargs["op2"]}"')
        else:
            self.cursor.execute(f"SELECT * FROM {kwargs['table']}")
        return self.cursor.fetchall()

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
                self.cursor.execute(f'INSERT INTO users(id, user_name, fl_name) VALUES ({kwargs["user_id"]}, "{kwargs["user_name"]}", "{kwargs["fl_name"]}")')
                self.conn.commit()

    def get_status_id(self, **kwargs):
        self.cursor.execute(f'SELECT status_id FROM users WHERE id = {kwargs["user_id"]}')
        status_id = self.cursor.fetchall()[0][0]
        return status_id


db = DataBase()