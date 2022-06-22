import sqlite3


# объект доступа к данным поисков
class SearchDao:
    def __init__(self, sqlite_connection):
        self.sqlite_connection = sqlite_connection

    def get_search(self, requester_id):
        cursor = self.sqlite_connection.cursor()
        sqlite_select_query = "SELECT * FROM searches WHERE vk_id=?"
        result = cursor.execute(sqlite_select_query, (requester_id,))
        search = result.fetchone()
        cursor.close()
        return search

    def save_search(self, requester_id, age_from, age_to, sex, city):
        cursor = self.sqlite_connection.cursor()
        sqlite_insert_query = '''INSERT OR REPLACE INTO searches
                                (vk_id, age_from, age_to, sex, city)
                                VALUES (?,?,?,?,?);'''
        cursor.execute(sqlite_insert_query, (requester_id, age_from, age_to, sex, city))
        self.sqlite_connection.commit()

        cursor.close()


class MatchDao:
    def __init__(self, sqlite_connection):
        self.sqlite_connection = sqlite_connection

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
        search_ddl_query = """CREATE TABLE IF NOT EXISTS searches (
                           vk_id integer PRIMARY KEY,
                           age_from integer NOT NULL,
                           age_to integer NOT NULL, 
                           sex VARCHAR (1) NOT NULL,
                           city VARCHAR (50) NOT NULL)
               """
        cursor.execute(search_ddl_query)
        cursor.close()

    def __del__(self):
        if self.sqlite_connection:
            self.sqlite_connection.close()

    def get_match_dao(self):
        return MatchDao(self.sqlite_connection)

    def get_search_dao(self):
        return SearchDao(self.sqlite_connection)
