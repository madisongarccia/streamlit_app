import plotly.express as px
import pandas as pd
import streamlit as st
import folium
from geopy.geocoders import Nominatim

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
    
map_sc = folium.Map(location=[34.052235, -118.243683], zoom_start=7)
geolocator = Nominatim(user_agent="southern_california")
cities_df = data['City']

for index, row in cities_df.iterrows():
    location = geolocator.geocode(row['City'] + ', Southern California')
    if location:
        folium.Marker(location=[location.latitude, location.longitude], popup=row['City']).add_to(map_sc)

map_sc.save('socal_cities.html')
st.write(open('socal_cities.html').read(), unsafe_allow_html=True)

# sort by salary and show distribution of highest paid roles
# to demonstrate what is possible as a data scientist
    
# How do your options change depending on work environment
    


