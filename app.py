import plotly.express as px
import pandas as pd
import streamlit as st

st.title('Data Curation App')

# Expander for where this data came from
with st.expander(label = 'Data Description'):
    st.write("""The data collected for this app was 
             found by scraping job postings from Indeed. 
             The job postings were filtered for Data Science
             positions, or anything similar in the Los Angeles area. 
             This app allows anyone the opportunity to explore the data gathered from
             this process, to gain a better understanding of the job 
             market in LA.""")
    
# sort by salary and show distribution of highest paid roles
# to demonstrate what is possible as a data scientist
    
# How do your options change depending on work environment
    


