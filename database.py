import sqlite3
from tkinter import CURRENT

connection = sqlite3.connect("cars_db.sqlite")
cursor = connection.cursor()

cursor.execute("""SELECT
car_models.model,
cars.car_color,
owners.name,
owners.card
FROM cars, car_models, owners
WHERE cars.owner_id = owners.id and cars.car_model_id = car_models.id and car_models.mark = \"Chevrolet\"""")

response = cursor.fetchall()

ELEMENT_LEN = 20

response_len = len(response)
response_el_len = len(response[0])

print(("+" + "-" * (ELEMENT_LEN + 1)) * response_el_len, end="+\n")
for i in response:
	print(end="| ")
	for j in i:
		print(f"{j: <20}", end="| ")
	print("\n" + ("+" + "-" * (ELEMENT_LEN + 1)) * response_el_len, end="+\n")

connection.close()