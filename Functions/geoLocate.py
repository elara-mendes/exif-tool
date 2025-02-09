from geopy.geocoders import Nominatim
from Functions.Colors import Colors
TEXT_RED, TEXT_GREEN, TEXT_YELLOW, TEXT_RESET = Colors()
import streamlit as st
# pip install geopy
# pip install opencage

@st.cache_data
def geoLocator(lat, lon):
    try:
        geoLocator = Nominatim(user_agent='my_geocoder', timeout=10)
        location = geoLocator.reverse((lat,lon), addressdetails=True, language='pt')
        return f'{location.address}'
    except Exception as  err:
        return f'{err}'


# endereco = geoLocator(latitude, longitude)

# print(endereco)

# zoom : int
# Level of detail required for the address, an integer in range from 0 (country level) to 18 (building level), default is 18.

# namedetails : bool
# If you want in Location.raw to include namedetails, set it to True. This will be a list of alternative names, including language variants, etc.