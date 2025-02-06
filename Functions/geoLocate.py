
from geopy.geocoders import Nominatim
# pip install geopy
# pip install opencage

geolocator = Nominatim(user_agent="my_geocoder")

latitude = 40.7128
longitude = -74.0060

location = geolocator.reverse((latitude, longitude))

print(location.address) 
# Example output: Flatiron Building, 175, 5th Avenue, Flatiron District, Manhattan, New York County, New York, 10010, United States of America