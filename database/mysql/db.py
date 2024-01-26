import pymysql

host = 'localhost'
user = 'root'
psd = 'zr2002081577'
port = 3306

MAX_SIZE = 1024 * 1024 * 1024


class Database:
    db = {}

    def __init__(self, db: str):
        if Database.db.__contains__(db):
            Database.db[db].__close(self)
        else:
            Database.db[db] = self
        self.db = db
        self.con = pymysql.connect(host=host, user=user, passwd=psd, port=port)
        self.cursor = self.con.cursor()
        self.__init_database__()

    def __init_database__(self):
        # set global max_allowed_packet = 1073741824;
        self.cursor.execute('set global max_allowed_packet = {0}'.format(MAX_SIZE))
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS ' + self.db)
        self.cursor.close()
        self.con.close()
        self.con = pymysql.connect(host=host, user=user, passwd=psd, port=port, database=self.db)
        self.cursor = self.con.cursor()

    def __close(self, new_db):
        Database.db[self.db] = new_db
        self.cursor.close()
        self.con.close()
        del self

    def create_table(self, table: str):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS ' + table)

    def table_is_none(self, table_name: str):
        self.cursor.execute(query='SELECT COUNT(*) FROM {}'.format(table_name))
        return self.cursor.fetchone()[0] == 0

    def insert(self, table: str, values: str):
        return self.cursor.execute('INSERT INTO {0} VALUES({1})'.format(table, values))

    def select(self, sel: str, table: str, condition: str):
        self.cursor.execute('SELECT {0} FROM {1} WHERE {2}'.format(sel, table, condition))
        return self.cursor.fetchall()

    def delete(self, table: str, condition: str):
        return self.cursor.execute('DELETE FROM {0} WHERE {1}'.format(table, condition))

    def save(self):
        self.con.commit()
