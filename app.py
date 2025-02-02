import pandas as pd
import folium
import sqlite3

from flask import Flask, request, render_template




app = Flask(__name__)
#base index.html
@app.route('/')
def home():
    return render_template("index.html")


"""
    <button onclick="sendID(1)">Select ID 1</button>
    <button onclick="sendID(2)">Select ID 2</button>
    <button onclick="sendID(3)">Select ID 3</button>
smth like this is on html page for example 

function sendID(id) {
            fetch("/process", {  
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ selectedID: id })  
            })

"""

# Connect to the database
conn = sqlite3.connect("database.db")

# Write your SQL query (change 'users' to your table name)
storeQuery = "SELECT storeID, storeName, long, lat FROM stores"
itemQuery = "SELECT storeID, item, price FROM items"

# Load data into a Pandas DataFrame
storeDF = pd.read_sql_query(storeQuery, conn)
itemDF = pd.read_sql_query(itemQuery, conn)
print(storeDF)
print(itemQuery)
# Close the connection
conn.close()


m = folium.Map(location=[40.497346, -74.440088], zoom_start=12)

itemLookingFor = ['bread', 'steak','califlower'] #this will be modified by webpage
itemLookingFor = 'bread'

"""
Filter DATABASES HERE 
"""
@app.route('/process')
def process():
    data = request.json.get("selectedName")  # Get ID from frontend
    itemLookingFor = int(data)  # Convert to integer for query
    filteredItems = itemDF[itemDF['item'] == itemLookingFor]
    filteredItems = filteredItems.sort_values(by='price', ascending=True) #make it so smallest price 
    cheepestPrice = filteredItems['price'].iat[0]
    cheepestID = filteredItems['storeID'].iat[0]
    filteredStore = storeDF[storeDF['storeID'] == cheepestID]

    for _, row in filteredStore.iterrows():

        lat = row['lat']
        print(f"lat {lat}")
        lon = row['long']
        print(f"lon {lon}")
        store_name = row['storeName']
        
        folium.CircleMarker(
            location=(lat, lon),
            radius=5,
            color="blue",
            fill=True,
            fill_color="cyan",
            fill_opacity=0.6,
            popup=f"Store Name: {store_name} |\n {itemLookingFor} ${cheepestPrice}",
        ).add_to(m)

    map_path = "templates/map.html"
    m.save(map_path)

    return render_template("map.html")

map_path = "templates/map.html"
m.save(map_path)
print("Interactive map saved as 'map.html'")
