import plotly.express as px
import pandas as pd
import streamlit as st
import folium
import geopy
from geopy.geocoders import Nominatim
from uszipcode import SearchEngine
from geopy.exc import GeocoderTimedOut

st.title('Los Angeles Job Explorer')

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

# sidebar with description of this app
with st.sidebar:
    st.header('Purpose of this App:')
    st.write("""
             This app was created to help students or anyone pursuing Data Science
              in the Los Angeles area, understand the current job market. 
             The app can help answer questions such as "What cities in LA can I expect to work in?" or
              "What is a realistic pay range for my experience?". 
             
             App Usage:\n
             This app includes an interactive map of Los Angeles, which marks all the cities containing 
             Data Science job postings. The user also has the ability to enter a chosen salary range to view a list of 
             both companies and titles that offer positions in that salary range. If you have a 
             specific company you hope to work for, there is an option to input a company name and view a list of 
             all the positions that company may be hiring for. At the bottom of the page, is a list of all the 
             companies that this website currently holds data on. 
             """)

# map of all the locations in my df
st.header('Question 1: What cities in LA County have positions available?')
st.subheader('Map of Cities in LA County That Offer Data Science Positions')
map_sc = folium.Map(location=[34.052235, -118.243683], zoom_start=9)
geolocator = Nominatim(user_agent="southern_california")
cities = data['City']
# dictionary of common cities to save time
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
            location = geolocator.geocode(city + ', Southern California', timeout=10)
            if location:
                folium.Marker(location=[location.latitude, location.longitude], popup=city).add_to(map_sc)
map_html = map_sc._repr_html_()
st.components.v1.html(map_html, width = 800, height=500)

# salary list to see which companies/jobs have that pay
st.header('Question 2: What Salary can I expect for a given job?')
st.write('Below will appear a list of jobs and companies for the given range')
popover = st.popover("Choose a Salary Range")
low = popover.checkbox('Show \$0 - \$50,000', False)
med = popover.checkbox('Show \$50,000  - \$100,000', False)
med2 = popover.checkbox('Show \$100,000 - \$350,000 ', False)
high = popover.checkbox('Show \$350,000 + ', False)

if low:
    st.subheader('Companies and Jobs with Salary Range \$0 - \$50,000')
    low_df = data[data['Pay'] <= 50000]
    jobs1 = low_df['Title']
    companies1 = low_df['Company']
    for job, company in zip(jobs1, companies1):
        st.write(f'{company}: {job}')  
if med:
    st.subheader('Companies and Jobs with Salary Range \$50,000  - \$100,000')
    med_df = data[(data['Pay'] >= 50000) & (data['Pay'] <= 100000)]
    jobs2 = med_df['Title']
    companies2 = med_df['Company']
    for job, company in zip(jobs2, companies2):
        st.write(f'{company}: {job}')
if med2:
    st.subheader('Companies and Jobs with Salary Range \$100,000 - \$350,000 ')
    med_df2 = data[(data['Pay'] >= 100000) & (data['Pay'] <= 350000)]
    jobs3 = med_df2['Title']
    companies3 = med_df2['Company']
    for job, company in zip(jobs3, companies3):
        st.write(f'{company}: {job}')
if high:
    st.subheader('Companies and Jobs with Salary Range \$350,000 +')
    high_df = data[data['Pay'] >= 350000]
    jobs4 = high_df['Title']
    companies4 = high_df['Company']
    for job, company in zip(jobs4, companies4):
        st.write(f'{company}: {job}')

# Choose a company and display title and pay
st.header('Question 3: What companies are hiring?')
st.subheader('Choose a company of interest to see if they are hiring:')
st.write('Hint: popular companies in LA are: UCLA, USC, Snapchat, or Boeing')
company = st.text_input(label ='Enter a company', value = 'ex: TikTok')

is_in_dataframe = data['Company'].str.lower().str.contains(company.lower()).any()
if is_in_dataframe:
    st.write(f'Yes {company.upper()} is currently hiring!')
    st.write(f'Here are the positions they are looking to fill:')
    df = data[data['Company'].str.lower().str.contains(company.lower())]
    positions = df['Title'].unique()
    pays = df['Pay'].unique()
    for position, pay in zip(positions, pays):
        st.write(f' - {position}')
else:
    st.write(f'Sorry, there currently is no data on {company.upper()}\'s job postings')

# final list of all companies considered in this website
company_names = data['Company'].sort_values().unique()
with st.expander(label='Click to see all companies with job data'):
    for name in company_names:
        st.write(name)
