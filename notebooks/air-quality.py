#%%
import pandas as pd
import folium
import webbrowser

# Load the data
data = pd.read_csv('Air_quality_geocoded.csv')
# Create a map centered at the mean latitude and longitude of the data
map = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=6)

# Add a marker to the map for each row in the data
for i, row in data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Place: {row['Place']}, Air Quality: {row['Air Quality']}"
    ).add_to(map)

# Save the map to an HTML file
map.save('map.html')

# Open the map in a web browser
webbrowser.open('map.html')
# %%
!pip install geopy -q
# %%
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

data = pd.read_csv('Air_quality_geocoded.csv')

# Create a geolocator object
geolocator = Nominatim(user_agent="myGeocoder")

# Create a rate limiter to avoid sending too many requests at once
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Define a function to geocode a place name
def get_location(place_name):
    location = geocode(place_name)
    if location:
        return pd.Series({'Latitude': location.latitude, 'Longitude': location.longitude})
    else:
        return pd.Series({'Latitude': None, 'Longitude': None})

# Apply the function to each row in the data
data[['Latitude', 'Longitude']] = data['Geo Place Name'].apply(get_location)
# %%
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

data = pd.read_csv('Air_quality.csv')

# Create a geolocator object
geolocator = Nominatim(user_agent="myGeocoder")

# Create a rate limiter to avoid sending too many requests at once
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Define a function to geocode a place name
def get_location(place_name):
    location = geocode(place_name)
    if location:
        return pd.Series({'Latitude': location.latitude, 'Longitude': location.longitude})
    else:
        return pd.Series({'Latitude': None, 'Longitude': None})

# Get the unique place names in the data
unique_place_names = data['Geo Place Name'].unique()

# Create a DataFrame to store the geocoded locations
locations = pd.DataFrame(unique_place_names, columns=['Geo Place Name'])

# Geocode the unique place names
locations[['Latitude', 'Longitude']] = locations['Geo Place Name'].apply(get_location)

# Merge the geocoded locations with the original data
data = pd.merge(data, locations, on='Geo Place Name')
# %%
data.to_csv('Air_quality_geocoded.csv', index=False)
# %%
import pandas as pd
import folium

data = pd.read_csv('Air_quality_geocoded.csv')

# Create a map centered at the mean latitude and longitude of the data
map = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=10)

# Add a marker to the map for each row in the data
for index, row in data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Geo Place Name']}: {row['Data Value']} {row['Measure Info']}"
    ).add_to(map)

# Display the map
map
# %%
import pandas as pd
import folium

data = pd.read_csv('Air_quality_geocoded.csv')

# Create a map centered at the mean latitude and longitude of the data
map = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=10)

# Add a marker to the map for each row in the data
for index, row in data.iterrows():
    if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Geo Place Name']}: {row['Data Value']} {row['Measure Info']}"
        ).add_to(map)

# Display the map
map
# %%
