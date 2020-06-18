import sqlite3

class Database:
    
    def __init__(self, db_name):
        self.conn = sqlite3.connect(f'{db_name}.db')

    def create_table(self, table_name, **col_name_types):
        self.c = self.conn.cursor()
        col_type = self.__format_string(**col_name_types)
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}(id INTEGER PRIMARY KEY AUTOINCREMENT, {col_type})''')
        self.conn.commit()

    def __format_string(self, **kwargs):
        string = ''
        for item in kwargs:
            string += f'{item} {kwargs[item]}, '
        return string[0: -2]

d = Database('testdb')
d.create_table('test2', name1='TEXT', name2='INTEGER')
