from geopy.geocoders import Nominatim
import streamlit as st

@st.cache_data
def geoLocator(lat, lon):
    try:
        geoLocator = Nominatim(user_agent='my_geocoder', timeout=10)
        location = geoLocator.reverse((lat,lon), addressdetails=True, language='pt')
        return f'{location.address}'
    except Exception as  err:
        return f'{err}'