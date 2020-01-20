import sqlite3
from sql_base import SQLBase


class Scores(SQLBase):
    def __init__(self, table="scores", columns=('id', 'reputation'), db_file='data.db', auto_connect=False):
        super().__init__(table, columns, db_file, auto_connect)

    def init_table(self):
        self.conn.execute("CREATE TABLE IF NOT EXISTS scores ("
                          "id integer PRIMARY KEY, "
                          "reputation integer"
                          ")")

    def get_rep(self, id_str):
        return self.get(id_str, "reputation")

    def add_rep(self, id_str, rep):
        target = self.get(id_str, "reputation")[0] + rep
        return self.update(id_str, {"reputation": target})

if __name__ == "__main__":
    testTable = Scores(auto_connect=True)
    testTable.init_table()
    print(testTable.get_all())
