import sqlite3
db = sqlite3.connect("database.db")
cursor = db.cursor()  # Create a cursor object to interact with the database
cursor.execute("SELECT * FROM stores")  # Replace "users" with your table name
rows = cursor.fetchall()

for row in rows:
    print(row)

print("\n \n")
cursor.execute("SELECT * FROM items")  # Replace "users" with your table name
rows = cursor.fetchall()

for row in rows:
    print(row)