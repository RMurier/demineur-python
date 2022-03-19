import os
import sqlite3
from sqlite3.dbapi2 import connect

class DataBaseHandler():
    def __init__(self, database_name: str):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.con.row_factory = sqlite3.Row
    
    def get_user(self, username: str):
        cursor = self.con.cursor()
        query = "SELECT * FROM users WHERE username = ?;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return list(result)