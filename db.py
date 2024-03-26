import logging
import traceback

import psycopg2
import config


class DataBase(object):
    def __init__(self):
        self.conn = psycopg2.connect(
            host=config.PGHOST,
            database=config.PGDATABASE,
            user=config.PGUSER,
            port=config.PGPORT,
            password=config.PGPASS)

        self.cursor = self.conn.cursor()

    def check_record(self, message):
        try:
            self.check_connection()

            self.cursor.execute(""" SELECT id FROM mfo_users WHERE id = %s """, [message.from_user.id])
            user_id = self.cursor.fetchone()
            self.conn.commit()

            if user_id is None:
                name = ''
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name
                if first_name:
                    name = name + first_name
                if last_name:
                    if name:
                        name = name + ' ' + last_name
                    else:
                        name = last_name

                self.cursor.execute("""INSERT INTO mfo_users (id, name, username) VALUES (%s, %s, %s)""", (message.from_user.id, name, message.from_user.username))
                self.conn.commit()

        except:
            logging.error(traceback.format_exc())
            return

    def get_all_users(self):
        try:
            self.check_connection()

            self.cursor.execute(f"""SELECT id FROM mfo_users""")
            all_ids = self.cursor.fetchall()
            return all_ids

        except:
            logging.error(traceback.format_exc())
            return []

    def save_number(self, user_id, number):
        try:
            self.check_connection()

            self.cursor.execute(f"""UPDATE mfo_users SET number = %s WHERE id = %s""", (number, user_id))
            self.conn.commit()

        except:
            logging.error(traceback.format_exc())

    def check_connection(self):
        if self.conn.closed or self.cursor.closed:
            if not self.conn.closed:
                self.conn.close()
            if not self.cursor.closed:
                self.cursor.close()

            self.conn = psycopg2.connect(
                host=config.PGHOST,
                database=config.PGDATABASE,
                user=config.PGUSER,
                port=config.PGPORT,
                password=config.PGPASS)

            self.cursor = self.conn.cursor()

    def check_number(self, user_id):
        try:
            self.check_connection()

            self.cursor.execute(""" SELECT number FROM mfo_users WHERE id = %s """, [user_id])
            number = self.cursor.fetchone()[0]
            self.conn.commit()

            if number:
                return True

        except:
            logging.error(traceback.format_exc())




db = DataBase()