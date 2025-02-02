import pandas as pd
import folium
import sqlite3

from flask import Flask, request, render_template

stores_df = pd.read_csv("stores.csv")  # Store locations
items_df = pd.read_csv("items.csv")  # Item prices
zipcodes_df = pd.read_csv("zipcodes.csv")  # Zip code locations


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
"""
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

"""
m = folium.Map(location=[40.497346, -74.440088], zoom_start=12)



"""
Filter DATABASES HERE 
"""
@app.route('/process')
def process():
    data = request.json.get("selectedName")  # Get ID from frontend
    selected_item = data.lower().strip()

    filtered_items = items_df[items_df['item'].str.lower() == selected_item]
    cheapest_item = filtered_items.sort_values(by='price').iloc[0]
    cheapest_store_id = cheapest_item['storeID']
    cheapest_price = cheapest_item['price']

    # Get store details for the cheapest store
    store_info = stores_df[stores_df['storeID'] == cheapest_store_id]
    #Coordinates of the store with smallest price 
    lat = store_info['lat'].values[0]
    lon = store_info['long'].values[0]
    store_name = store_info['storeName'].values[0]


    #Zip code center 
    map_center = zipcodes_df.iloc[0]  
    map_lat, map_lon = map_center['lat'], map_center['long']

    m = folium.Map(location=[map_lat, map_lon], zoom_start=12)
    '''
    filteredItems = itemDF[itemDF['item'] == itemLookingFor]
    filteredItems = filteredItems.sort_values(by='price', ascending=True) #make it so smallest price 
    cheepestPrice = filteredItems['price'].iat[0]
    cheepestID = filteredItems['storeID'].iat[0]
    filteredStore = storeDF[storeDF['storeID'] == cheepestID]
    '''

    folium.CircleMarker(
        location=(lat, lon),
        popup=f"Store: {store_name}<br>{selected_item.capitalize()} - ${cheapest_price}",
        icon=folium.Icon(color="green"),
    ).add_to(m)
    """
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
    """
    #Mb change
    map_path = "templates/map.html"
    m.save(map_path)

    return render_template("map.html")

#dunno wtf iz diz nuts
if __name__ == '__main__':
    app.run(debug=True)

    
"""
map_path = "templates/map.html"
m.save(map_path)
print("Interactive map saved as 'map.html'")
"""

