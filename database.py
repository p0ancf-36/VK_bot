import sqlite3
from tkinter import CURRENT

connection = sqlite3.connect("cars_db.sqlite")
cursor = connection.cursor()

cursor.execute("""
	CREATE TABLE IF NOT EXISTS owners (
		id INTEGER PRIMARY KEY,
		name TEXT,
		card INTEGER
	)
""")
cursor.execute("""
	CREATE TABLE IF NOT EXISTS car_models (
		id INTEGER PRIMARY KEY,
		mark TEXT,
		model TEXT,
		prod_country TEXT
	)
""")
cursor.execute("""
	CREATE TABLE IF NOT EXISTS cars (
		id INTEGER PRIMARY KEY,
		owner_id INTEGER,
		car_number INTEGER,
		car_model_id INTEGER,
		car_color TEXT,

		FOREIGN KEY (owner_id) REFERENCES owners (id)
		FOREIGN KEY (car_model_id) REFERENCES car_models (id)
	)
""")

cursor.execute("""INSERT INTO owners VALUES (1, "Вася", 123)""")
cursor.execute("""INSERT INTO owners VALUES (2, "Ира", 124)""")
cursor.execute("""INSERT INTO owners VALUES (3, "Игорь", 125)""")
cursor.execute("""INSERT INTO owners VALUES (4, "Виктор", 126)""")
cursor.execute("""INSERT INTO owners VALUES (5, "Андрей", 127)""")

cursor.execute("""INSERT INTO car_models VALUES (1, "Toyota", "Camry", "Japan")""")
cursor.execute("""INSERT INTO car_models VALUES (2, "Lada", "Kalina", "Russia")""")
cursor.execute("""INSERT INTO car_models VALUES (3, "Chevrolet", "Camaro", "USA")""")
cursor.execute("""INSERT INTO car_models VALUES (4, "Lexus", "RX", "Japan")""")
cursor.execute("""INSERT INTO car_models VALUES (5, "Daewoo", "Matiz", "South Korea")""")

cursor.execute("""INSERT INTO cars VALUES (1, 1, 758, 1, "red")""")
cursor.execute("""INSERT INTO cars VALUES (2, 2, 176, 1, "white")""")
cursor.execute("""INSERT INTO cars VALUES (3, 2, 659, 2, "black")""")

cursor.execute("""INSERT INTO cars VALUES (4, 3, 134, 3, "yellow")""")
cursor.execute("""INSERT INTO cars VALUES (5, 4, 777, 3, "black")""")
cursor.execute("""INSERT INTO cars VALUES (6, 5, 324, 4, "gray")""")
cursor.execute("""INSERT INTO cars VALUES (7, 5, 333, 2, "brown")""")
cursor.execute("""INSERT INTO cars VALUES (8, 2, 432, 5, "green")""")

connection.commit()

connection.close()