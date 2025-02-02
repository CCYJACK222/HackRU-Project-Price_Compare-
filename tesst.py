import pandas as pd
import folium
from flask import Flask, request, render_template

app = Flask(__name__)

# Load CSV data into Pandas DataFrames
stores_df = pd.read_csv("stores.csv")
items_df = pd.read_csv("items.csv")
zipcodes_df = pd.read_csv("zipcodes.csv")  # For map centering

@app.route('/')
def home():
    return render_template("index.html")  # Load input form

@app.route('/process', methods=['POST'])
def process():
    data = request.json.get("selectedID")  # Get ID from frontend
    selected_id = int(data)  # Convert to integer

    # Filter the store information
    store_info = stores_df[stores_df['storeID'] == selected_id]
    
    if store_info.empty:
        return f"<h2>No store found for ID {selected_id}.</h2><a href='/'>Go Back</a>"

    # Get store details
    lat = store_info['lat'].values[0]
    lon = store_info['long'].values[0]
    store_name = store_info['storeName'].values[0]

    # Get item prices for the selected store
    store_items = items_df[items_df['storeID'] == selected_id]
    
    items_list = ""
    for _, row in store_items.iterrows():
        items_list += f"{row['item']} - ${row['price']}<br>"

    # Get map center from zipcodes.csv (default to first row if empty)
    map_center = zipcodes_df.iloc[0]  # Default center from first zip code
    map_lat, map_lon = map_center['lat'], map_center['long']

    # Create a map centered on the store
    m = folium.Map(location=[map_lat, map_lon], zoom_start=12)

    folium.Marker(
        location=(lat, lon),
        popup=f"Store: {store_name}<br>{items_list}",
        icon=folium.Icon(color="blue"),
    ).add_to(m)

    # Save the map and return it
    map_path = "templates/map.html"
    m.save(map_path)

    return render_template("map.html")

if __name__ == '__main__':
    app.run(debug=True)
