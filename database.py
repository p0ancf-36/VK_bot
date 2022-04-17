import sqlite3
from tkinter import CURRENT

connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()

cursor.execute("""
	CREATE TABLE IF NOT EXISTS groups (
		id INTEGER PRIMARY KEY,
		name TEXT
	)
""")
cursor.execute("""
	CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY,
		chat_id INTEGER,
		group_id INTEGER,

		FOREIGN KEY (group_id) REFERENCES groups(id)
	)
""")

cursor.execute("INSERT INTO groups VALUES(1, \"friends\")")
cursor.execute("INSERT INTO groups VALUES(2, \"classmates\")")
cursor.execute("INSERT INTO groups VALUES(3, \"programmers\")")

connection.commit()

connection.close()