import plotly.express as px
import pandas as pd
import streamlit as st
import folium
from geopy.geocoders import Nominatim
from uszipcode import SearchEngine
from geopy.exc import GeocoderTimedOut

st.title('Data Curation App')

data = pd.read_csv('3-26.csv')


# Expander for where this data came from
with st.expander(label = 'Data Description'):
    st.write("""The data collected for this app was 
             found by scraping job postings from Indeed. 
             The job postings were filtered for Data Science
             positions, or anything similar in the Los Angeles area. 
             This app allows anyone the opportunity to explore the data gathered from
             this process, to gain a better understanding of the job 
             market in LA.""")


# map of all the locations in my df
st.title('Map of Cities in LA County That Offer Data Science Positions')
map_sc = folium.Map(location=[34.052235, -118.243683], zoom_start=7)
geolocator = Nominatim(user_agent="southern_california")
cities = data['City']
la_city_coordinates = {
    'Los Angeles': (34.052235, -118.243683),
    'Long Beach': (33.770050, -118.193740),
    'Santa Monica': (34.0194, -118.4912),
    'Beverly Hills': (34.0736, -118.4004),
    'Pasadena': (34.1478, -118.1445),
    'Glendale': (34.1425, -118.2551),
    'Santa Clarita': (34.3917, -118.5426),
    'Torrance': (33.8350, -118.3406),
    'Inglewood': (33.9617, -118.3531),
    'Downey': (33.9400, -118.1336),
    'Norwalk': (33.9022, -118.0817),
    'Compton': (33.8958, -118.2201),
    'Pomona': (34.0551, -117.7499),
    'West Hollywood': (34.0900, -118.3617),
    'Lakewood': (33.8506, -118.1332),
    'Whittier': (33.9792, -118.0328),
    'Burbank': (34.1808, -118.3089),
    'Redondo Beach': (33.8492, -118.3884),
    'Huntington Beach': (33.6603, -117.9992),
    'Anaheim': (33.8366, -117.9143),
    'El Segundo': (33.9192, -118.4165),
    'Culver City': (34.0211, -118.3965),
    'Hawthorne': (33.9164, -118.3526)
}
for city in cities:
    if isinstance(city, str):
        city = city.strip('\n, ')
        if city in la_city_coordinates:
            folium.Marker(location=la_city_coordinates[city], popup=city).add_to(map_sc)
        else:
            #print(f'city: {city}')
            location = geolocator.geocode(city + ', Southern California', timeout=10)
            if location:
                folium.Marker(location=[location.latitude, location.longitude], popup=city).add_to(map_sc)
map_html = map_sc._repr_html_()
st.components.v1.html(map_html, width = 800, height=600)

# sort by salary and show distribution of highest paid roles
# to demonstrate what is possible as a data scientist
    
# How do your options change depending on work environment
    


