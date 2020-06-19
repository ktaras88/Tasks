import sqlite3

class Database:
    
    def __init__(self, db_name):
        self.conn = sqlite3.connect(f'{db_name}.db')
        self.c = self.conn.cursor()
    
    def __format_string(self, **kwargs):
        string = ''
        for item in kwargs:
            string += f'{item} {kwargs[item]}, '
        return string[0: -2]

    def create_table(self, table_name, **col_name_types):
        try:
            col_type = self.__format_string(**col_name_types)
            self.c.execute(f'''CREATE TABLE {table_name}(id INTEGER PRIMARY KEY AUTOINCREMENT, {col_type})''')
            self.conn.commit()
            print(f'Table {table_name} was created')
        except sqlite3.OperationalError:
            print(f'Table {table_name} alredy exist')

    def drop_table(self, table_name):
        try:
            self.c.execute(f'DROP TABLE {table_name}')
            print(f'Table {table_name} was dropped')
        except sqlite3.OperationalError:
            print(f'Table {table_name} alredy dropped')

    def insert_into_table(self, table_name, **col_val):
        c_v = self.__format_insert(**col_val)
        self.c.execute(f'INSERT INTO {table_name} ({c_v[0]}) VALUES ({c_v[1]})')

    def __format_insert(self, **kwargs):
        string = ''
        string1 = ''
        for item in kwargs:
            string += f'{item}, '
            string1 += f'{kwargs[item]}, '
        return string[0: -2], string1[0:-2]


d = Database('database_test')
d.create_table('table_test', name1='TEXT', name2='INTEGER')
d.insert_into_table('table_test', name1='val1', name2='val2')