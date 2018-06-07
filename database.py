import os
import sqlite3

import requests

class Database():
    def __init__(self, dbname=os.path.join("db", "database.db")):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname, check_same_thread=False)
        self.conn.text_factory = str

    def connection(self, dbname):
        conn = sqlite3.connect(dbname)
        return conn

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def create_tables(self):
        cursor = self.cursor()
        sql = """
        DROP TABLE IF EXISTS user;
        DROP TABLE IF EXISTS server;
        

        CREATE TABLE server
        (
            server_id text PRIMARY KEY,
            server_name text,
            server_track_ggg integer,
            server_channel text,
            server_most_recent_item_id text
        );

        CREATE TABLE user
        (
            user_id integer PRIMARY KEY AUTOINCREMENT,
            user_name text,
            user_league text
        );
        """
        cursor.executescript(sql)
        self.commit()

    def add_server(self, server, channel):
        sql = "INSERT INTO server(server_id, server_name, server_track_ggg, server_channel) VALUES (?, ?, ?, ?)"
        self.cursor().execute(sql, (server.id, server.name, 1, channel.id))
        self.commit()

    def set_server_ggg(self, server, value, channel):
        sql = "UPDATE server SET server_track_ggg = ?, server_channel = ? WHERE server_id = ?"
        self.cursor().execute(sql, (value, channel.id, server.id))
        self.commit()

    def remove_server(self, server):
        sql = "DELETE FROM server WHERE server_id = ?"
        self.cursor().execute(sql, (server.id,))
        self.commit()

    def check_server_exists(self, server):
        sql = "SELECT * FROM server WHERE server_id = ?"
        cursor = self.cursor()
        cursor.execute(sql, (server.id,))
        data = cursor.fetchone()
        if data:
            return True
        else:
            return False

    def get_server_ggg(self, server):
        pass

    def set_league_db(self, user, league):
        sql = "UPDATE user SET user_league = ? WHERE user_id = ?"
        self.cursor().execute(sql, (league, user.id))
        self.commit()

    def add_user(self, user, league="Standard", name=""):
        sql = "INSERT INTO user(user_id, user_league, user_name) VALUES (?, ?, ?)"
        self.cursor().execute(sql, (user.id, league, name))
        self.commit()

    def get_league(self, user):
        sql = "SELECT user_league FROM user WHERE user_id = ?"
        cursor = self.cursor()
        cursor.execute(sql, (user.id,))
        data = cursor.fetchone()
        if data:
            return data[0]
        else:
            return None

    def check_user_exists(self, user):
        sql = "SELECT * FROM user WHERE user_id = ?"
        cursor = self.cursor()
        cursor.execute(sql, (user.id,))
        data = cursor.fetchone()
        if data:
            return True
        else:
            return False

    def get_league_list(self):
        # This is a static method, but I am unsure which scope is best to place this method, so for now, it stays here
        """
        This gets a list of leagues from the official site api

        :return: list of strings
        """
        url = "http://www.pathofexile.com/api/trade/data/leagues"
        r = requests.get(url).json()
        if r.get("result"):
            return [x.get("id") for x in r.get("result")]
        else:
            return []

if __name__ == "__main__":
    # We want to create the database directory in the top level
    db_path = os.path.join("db", "database.db")
    try:
        db = Database(db_path)
    except sqlite3.OperationalError:
        os.mkdir("db")
        db = Database(db_path)
    db.create_tables()