import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
import os 

DB_PATH = "./db"

os.makedirs(DB_PATH, exist_ok=True)

class MySQLCheckpointer(SqliteSaver):
    def __init__(self, name: str):
        super().__init__(sqlite3.connect(f"{DB_PATH}/{name}_checkpoint.sqlite",check_same_thread=False))