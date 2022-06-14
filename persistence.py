import sqlite3


class Persistence:
    def __init__(self, db_uri='sqlite_vk_bot.sqlite'):
        self.sqlite_connection = sqlite3.connect(db_uri)
        cursor = self.sqlite_connection.cursor()
        match_ddl_query = """CREATE TABLE IF NOT EXISTS matches (
                    vk_id integer,
                    requester_id integer,
                    CONSTRAINT match_pk primary key (vk_id, requester_id))
        """
        cursor.execute(match_ddl_query)

    def __del__(self):
        if self.sqlite_connection:
            self.sqlite_connection.close()

    def check_uniqueness(self, vk_id, requester_id) -> bool:
        cursor = self.sqlite_connection.cursor()
        sqlite_select = """SELECT * FROM matches WHERE vk_id=? AND requester_id=?"""
        result = cursor.execute(sqlite_select, (vk_id, requester_id))
        return result.fetchone() is None

    def save_match(self, vk_id, requester_id):
        cursor = self.sqlite_connection.cursor()
        sqlite_insert_with_param = '''INSERT INTO matches
                                        (vk_id, requester_id)
                                        VALUES (?,?);'''
        cursor.execute(sqlite_insert_with_param, (vk_id, requester_id))
        self.sqlite_connection.commit()

        cursor.close()
