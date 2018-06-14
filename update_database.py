"""
This is just for updating the database, not sure how to handle this in future, but ill deal with it as it comes

"""

from database import Database

def update(db):
    cursor = db.cursor()
    sql = """
    DROP TABLE IF EXISTS server;
    CREATE TABLE server
    (
        server_id text PRIMARY KEY,
        server_name text,
        server_track_ggg integer,
        server_channel text,
        server_track_hash text
    );
        """

    cursor.executescript(sql)
    db.commit()

if __name__ == "__main__":
    db = Database()
    update(db)
