import pymysql

host = 'localhost'
user = 'root'
psd = 'zr2002081577'
port = 3306


class Database:
    db = None

    def __init__(self, db: str):
        if Database.db is not None:
            Database.db.__close(self)
        else:
            Database.db = self
        self.db = db
        self.con = pymysql.connect(host=host, user=user, passwd=psd, port=port)
        self.cursor = self.con.cursor()
        self.__init_database__()

    def __init_database__(self):
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS ' + self.db)
        self.cursor.close()
        self.con.close()
        self.con = pymysql.connect(host=host, user=user, passwd=psd, port=port, database=self.db)
        self.cursor = self.con.cursor()

    def __close(self, new_db):
        Database.db = new_db
        self.cursor.close()
        self.con.close()
        del self

    def create_table(self, table: str):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS ' + table)

    def table_is_none(self, table_name: str):
        self.cursor.execute(query='SELECT COUNT(*) FROM {}'.format(table_name))
        return self.cursor.fetchone()[0] == 0

    def insert(self, first: str, second: str):
        self.cursor.execute('INSERT INTO {0} VALUES({1})'.format(first, second))
        self.con.commit()
