import sqlite3

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    username BLOB NOT NULL
) WITHOUT ROWID ;"""

GET_USERNAME = "SELECT username FROM players WHERE id = {};"
UPDATE_USERNAME = "UPDATE players SET username = \"{}\" WHERE id = {};"
INSERT_USERNAME = "INSERT INTO players (id, username) VALUES ({}, \"{}\");"

class UserNotFoundException(Exception):
    def __init__(self, _id) -> None:
        super().__init__(f"user with id {_id} not found")

class XonoticIdUsernameDatabase():
    def __init__(self, path) -> None:
        self.connection = sqlite3.connect(path)
        self.connection.execute(CREATE_TABLE).close()

    def get_username(self, _id):
        query = GET_USERNAME.format(_id)
        cursor = self.connection.execute(query)
        fetch = cursor.fetchone()
        if not fetch:
            raise UserNotFoundException(_id)
        return str(fetch[0])

    def set_username(self, _id, username):
        query = UPDATE_USERNAME.format(username, _id)
        c = self.connection.execute(query)
        if not c.rowcount:
            c.close()
            query = INSERT_USERNAME.format(_id, username)
            self.connection.execute(query).close()
            print(f"user {_id} did not exist, inserted data")
        else:
            print(f"user {_id} username updated")

    def close(self):
        self.connection.commit()
        self.connection.close()