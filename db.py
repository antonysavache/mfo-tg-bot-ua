import psycopg2
import config


class DataBase(object):
    def __init__(self):
        # super(DataBase, self).__init__()
        # self.db = sqlite3.connect('DataBase.db')
        # self.sql = self.db.cursor()
        self.conn = psycopg2.connect(
            host=config.PGHOST,
            database=config.PGDATABASE,
            user=config.PGUSER,
            port=config.PGPORT,
            password=config.PGPASS)

        self.cursor = self.conn.cursor()

    def check_record(self, id):
        self.cursor.execute(""" SELECT id FROM mfo_users WHERE id = %s """, [id])
        user_id = self.cursor.fetchone()
        self.conn.commit()

        if user_id is None:
            self.cursor.execute("""INSERT INTO mfo_users VALUES (%s)""", [id])
            self.conn.commit()

    def get_current(self):
        self.cursor.execute(""" SELECT page FROM mfo_current_page """)
        return self.cursor.fetchone()[0]


    def update_cur_page(self, number):
        self.cursor.execute(""" UPDATE mfo_current_page SET page = %s""", [number])
        self.conn.commit()


    def get_all_users(self):
        self.cursor.execute(f"""SELECT id FROM mfo_users""")
        all_ids = self.cursor.fetchall()
        return all_ids

db = DataBase()
