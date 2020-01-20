import sqlite3


class SQLBase:
    def __init__(self, table, columns, db_file, auto_connect):
        self.conn = None
        self.c = None
        self.db_file = db_file
        self.table = table
        self.columns = columns
        if auto_connect:
            self.connect()
            self.init_table()

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()

    @classmethod
    def init_table(cls):
        pass

    def get(self, id_str: int, columns: str = '*'):
        self.c.execute("SELECT {0} FROM {1} WHERE id=:id".format(columns, self.table), {'id': id_str})
        return self.c.fetchone()

    def get_all(self, columns: str = '*'):
        self.c.execute("SELECT {0} FROM {1}".format(columns, self.table))
        return self.c.fetchall()

    def add_element(self, id_str: int, values: dict = None, default=0):
        if values is None:
            values = {}

        values['id'] = id_str

        for column in self.columns:
            if column not in values:
                values[column] = default

        self.c.execute(
            "INSERT INTO {0} VALUES {1}".format(self.table,
                                                tuple(map(lambda col: ':' + col, self.columns))).replace("'", ''),
            values
        )
        return values

    def update(self, id_str: int, values: dict):
        values['id'] = id_str

        self.c.execute(
            "UPDATE {0} SET {1} WHERE id=:id".format(
                self.table,
                tuple(map(lambda col: col + ' = :' + col, values))).replace("'", '').replace('(', '').replace(')', ''),
            values
        )
        return values
