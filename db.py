import sqlite3


class DataBase(object):
    def __init__(self):
        super(DataBase, self).__init__()
        self.db = sqlite3.connect('DataBase.db')
        self.sql = self.db.cursor()

    def check_record(self, id):
        self.sql.execute("SELECT id FROM users WHERE id = ?", (id,))
        if self.sql.fetchone() is None:
            return False
        else:
            return True

    def add_user(self, user_id):
        self.sql.execute(f"INSERT INTO users VALUES ('{user_id}')")
        self.db.commit()


    def get_current(self):
        for i in self.sql.execute("SELECT current FROM current_page"):
            return i[0]


    def update_cur_page(self, number):
        self.sql.execute("UPDATE current_page SET current = ?", (number,))
        self.db.commit()


    def get_all_users(self):
        users = []
        for i in self.sql.execute("SELECT id FROM users"):
            users.append(i[0])
        return users

db = DataBase()
