from asyncio import QueueEmpty
import os
import re
import sqlite3
from sqlite3.dbapi2 import connect

class DataBaseHandler():
    def __init__(self, database_name: str):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.con.row_factory = sqlite3.Row
    
    def userExist(self, username: str):
        cursor = self.con.cursor()
        query = "SELECT COUNT(*) FROM users WHERE username = ?;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        for elem in result:
            return elem == 1

    def getUser(self, username: str):
        cursor = self.con.cursor()
        query = "SELECT * FROM users WHERE username = ?;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close
        return list(result)

    def createUser(self, username: str):
        cursor = self.con.cursor()
        query = "INSERT INTO users(username) VALUES (?) RETURNING id"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        self.con.commit()
        cursor.close()
        for elem in result:
            return elem

    def insertScore(self, id, score):
        cursor = self.con.cursor()
        query = "INSERT INTO score(id, score) VALUES (?, ?)"
        cursor.execute(query, (id, score))
        self.con.commit()
        cursor.close()

    def scoreboard(self):
        cursor = self.con.cursor()
        query = "SELECT username, score FROM score JOIN users USING(id) ORDER BY score LIMIT(5)"
        cursor.execute(query)
        result = list(map(list, cursor.fetchall()))
        cursor.close()
        return result