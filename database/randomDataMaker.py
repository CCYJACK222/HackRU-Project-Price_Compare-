import random
import sqlite3

store1 = [1, "Price is Wrong", 40.494772, -74.446492, "06483"]
store2 = [2, "Small Lots", 40.497158, -74.449282, "06483"]

db = sqlite3.connect("database.db")  # Creates or connects to an SQLite database
cursor = db.cursor()  # Create a cursor object to interact with the database

cursor.execute("INSERT INTO stores (storeID, storeName, lat, long, zipcode) VALUES (?, ?, ?, ?, ?)", 
               (store1[0],store1[1],store1[2],store1[3],store1[4]))

cursor.execute("INSERT INTO stores (storeID, storeName, lat, long, zipcode) VALUES (?, ?, ?, ?, ?)", 
               (store2[0],store2[1],store2[2],store2[3],store2[4]))

items = ["bread","milk", "chicken", "steak", "potato", "brocalli","califlower"]

for i in items:
    storeID = 1
    price = random.uniform(.05, 10.00)
    cursor.execute("INSERT INTO items (storeID, item, price) VALUES (?, ?, ?)", 
               (storeID, i, price))
    
for i in items:
    storeID = 2
    price = random.uniform(.05, 10.00)
    cursor.execute("INSERT INTO items (storeID, item, price) VALUES (?, ?, ?)", 
               (storeID, i, price))
    
db.commit()  # Save changes
cursor.close()