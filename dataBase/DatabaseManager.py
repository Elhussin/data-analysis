import sqlite3
import os
import sys


class DatabaseManager:
    def __init__(self,db_name ):
        self.db_name =db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """
        إنشاء جدول بناءً على اسم الجدول وتعريف الأعمدة
        :param table_name: اسم الجدول
        :param columns: قائمة تحتوي على تعريفات الأعمدة (اسم العمود + النوع)
        """
        column_definitions = ", ".join(columns)
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {column_definitions}
        );
        '''
        self.cursor.execute(query)
        self.conn.commit()

    def create_all_tables(self, table_definitions):
        """
        إنشاء جميع الجداول بناءً على قائمة تعريفات الجداول
        :param table_definitions: قائمة تحتوي على تعريفات الجداول
        """
        for table_def in table_definitions:
            self.create_table(table_def['table_name'], table_def['columns'])

    def __del__(self):
        self.conn.close()

table_definitions = [
    {
        "table_name": "Branches",
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "branch_name TEXT NOT NULL",
            "branch_location TEXT",
            "branch_phone TEXT",
            "status INTEGER",
            "date_start DATETIME DEFAULT CURRENT_TIMESTAMP",
            "last_update DATETIME DEFAULT CURRENT_TIMESTAMP"
        ]
    },
    {
        "table_name": "Orders",
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "Serial INTEGER",
            "branch INTEGER",
            "user INTEGER",
            "status INTEGER",
            "date_send TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "updated_at TIMESTAMP",
            "date_at_lap TIMESTAMP",
            "date_in_shop TIMESTAMP",
            "date_dilvery TIMESTAMP",
            "FOREIGN KEY (branch) REFERENCES Branches(id) ON DELETE SET NULL ON UPDATE CASCADE",
            "FOREIGN KEY (user) REFERENCES Users(id) ON DELETE SET NULL ON UPDATE CASCADE"
        ]
    },
    { 
        "table_name": "users",
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "username TEXT UNIQUE NOT NULL",
            "password TEXT NOT NULL",
            "full_name TEXT NOT NULL",
            "email TEXT NOT NULL",
            "status BOOLEAN DEFAULT TRUE",
            "date TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "user_type TEXT DEFAULT 'User'",
            "last_update TIMESTAMP"
        ]
    },
    {
        "table_name": "sessions",
        "columns": [
            "session_id INTEGER PRIMARY KEY AUTOINCREMENT",
            "user_id INTEGER",
            "login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "is_active BOOLEAN DEFAULT TRUE",
            "FOREIGN KEY(user_id) REFERENCES users(id)"
        ]
    },
    {
        "table_name": "Manager",
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "branch INTEGER",
            "user INTEGER",
            "state INTEGER",
            "date_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "date_end TIMESTAMP",
            "FOREIGN KEY (branch) REFERENCES Branches(id) ON DELETE SET NULL ON UPDATE CASCADE",
            "FOREIGN KEY (user) REFERENCES Users(id) ON DELETE SET NULL ON UPDATE CASCADE"
        ]
    }
]

