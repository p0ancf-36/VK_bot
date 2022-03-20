import sqlite3

connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS phrases(
	id INTEGER PRIMARY KEY NOT NULL,
	phrase TEXT,
	answer TEXT
)
""")
# cursor.execute("INSERT INTO phrases VALUES (1, \"Привет\", \"И тебе привет\")")
# cursor.execute("INSERT INTO phrases VALUES (2, \"Как дела?\", \"Хорошо\")")
# cursor.execute("INSERT INTO phrases VALUES (3, \"Как дела?\", \"А как у тебя?\")")

# connection.commit()

cursor.execute("SELECT * FROM phrases")
for i in cursor.fetchall():
	for j in i:
		print(j, end="\t")
	print()

connection.close()