import sqlite3
from datetime import timedelta

from sql_base import SQLBase
import settings



class Contributions(SQLBase):
    def __init__(self, table, db_file='data.db', auto_connect=False):
        columns = tuple(["id", "quota"] + settings.COLLECTIONS)
        super().__init__(table, columns, db_file, auto_connect)

    def init_table(self):
        collection_columns = " integer,".join(settings.COLLECTIONS) + " integer"
        self.conn.execute("CREATE TABLE IF NOT EXISTS {0} ("
                          "id integer PRIMARY KEY, "
                          "quota integer, "
                          "{1}"
                          ")".format(self.table, collection_columns))
        #TODO: if any userid in -(settings.REPO_UPDATE_EVENTS[::-1].total_seconds) exists in table, read result of it,
        # else put all zeros at userid -1


    def log_current_cycle(self, time, strike):
        pass
        #TODO: store current cycle under -time, and update user strike for spamming after quota reached

    def contribute(self, id_str:int, values: dict, admin=False):
        pass
        #TODO: if not exist, add ele with settings.[DAILY|ADMIN]_UPDATE_QUOTA, and update cycle

    def rep_delta(self):
        pass
        #TODO: called only when -(settings.REPO_UPDATE_EVENTS[-1].total_seconds) is populated, add negative quota as strikes

if __name__ == "__main__":
    testTable = Contributions("test_contribution", auto_connect=True)
    print(testTable.get_all())
