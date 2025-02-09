from exif import Image
import requests
import folium
import streamlit as st
from streamlit_folium import st_folium
from Functions.pythonGPT import pythonGPT
from Functions.Colors import Colors
from geopy.geocoders import Nominatim
from Functions.geoLocate import geoLocator
from datetime import datetime
from Functions.pythonGPT import knowMore
from Functions.textColor import textColor
from Functions.todayInfo import displayTime
from Functions.getWeather import getWeather
from dotenv import load_dotenv
import os
load_dotenv()
TEXT_RED, TEXT_GREEN, TEXT_YELLOW, TEXT_RESET = Colors()

# Evitando duplicação de texto no terminal, pelo PythonGPT pegar as mesmas informações.
with open('img/IMG_20250205_174349.jpg', 'rb') as image_file:
    my_image = Image(image_file)
    # print(f"Longitude: {my_image.gps_longitude} Ref: {my_image.gps_longitude_ref}")
    # print(f"Latitude: {my_image.gps_latitude} Ref: {my_image.gps_latitude_ref}")
    # print(f'Data e hora: {my_image.datetime_original}')
    # print(f'Celular : {my_image.make}')

horarioDaFoto = my_image.datetime_original
horaFormatada = horarioDaFoto.replace(':','/')
print(horaFormatada)
data, hora = horarioDaFoto.split(' ')
celular = my_image.make
modelo = my_image.model

# My ugly way!
print(f'{TEXT_RED} Informações {TEXT_RESET} ')

longitude_test = my_image.gps_longitude[0] + (my_image.gps_longitude[1] / 60) + (my_image.gps_longitude[2] / 3600)

if my_image.gps_longitude_ref == "W":
    longitude_test_str = "-" + str(longitude_test)
else:
    longitude_test_str = str(longitude_test)

longitude_list_mode = [int(i) for i in longitude_test_str if i.isdigit()]

# Minutes
minutes = [0, longitude_list_mode[2],longitude_list_mode[3], longitude_list_mode[4], longitude_list_mode[5]]
sub_minutes = int(("".join(str(i) for i in minutes)))*60
ml = [int(i) for i in str(sub_minutes)]

ml_calc = [ml[2], ml[3], ml[4]]
ml_lp = int(("".join(str(i) for i in ml_calc))) * 60
ml_fm = str(ml_lp).replace('0', '')

if my_image.gps_longitude_ref == "W":
    longitude_calc = f"""-{longitude_list_mode[0]}{longitude_list_mode[1]}º{ml[0]}{ml[1]}'{ml_fm[:2] + "." + ml_fm[2:]}"{my_image.gps_longitude_ref}"""
else:
    longitude_calc = f"""{longitude_list_mode[0]}{longitude_list_mode[1]}º{ml[0]}{ml[1]}'{ml_fm[:2] + "." + ml_fm[2:]}"{my_image.gps_longitude_ref}"""

# 43 degrees / 24.906(0.4151/60) / 24 minutes / 906 remainder(*60) / 54.36 seconds = 43º24'54.36" W // Calc here!
# Smart way!

latitude_test = my_image.gps_latitude[0] + (my_image.gps_latitude[1] / 60) + (my_image.gps_latitude[2] / 3600)

if my_image.gps_latitude_ref == "S":
    latitude_test_str = "-" + str(latitude_test)
else:
    latitude_test_str = str(latitude_test)

latitude_list_mode = [int(i) for i in latitude_test_str if i.isdigit()]

decimal_part = latitude_test - int(latitude_test)
degrees = int(latitude_test)
minutes = int(decimal_part * 60)
seconds = round((decimal_part * 60 - minutes) * 60, 4)

if my_image.gps_latitude_ref == "S":
    latitude_calc = f"-{latitude_list_mode[0]}{latitude_list_mode[1]}º{minutes}'{seconds}\"{my_image.gps_latitude_ref}"
else:
    latitude_calc = f"{latitude_list_mode[0]}{latitude_list_mode[1]}º{minutes}'{seconds}\"{my_image.gps_latitude_ref}"

print(f'{TEXT_YELLOW}={TEXT_RESET}'*60)

# Fixed
print(f'Latitude: {latitude_calc} Longitude: {longitude_calc}')
print(f'{TEXT_YELLOW} PYTHON GPT {TEXT_RESET}')
# knowMore(latitude_test_str, longitude_test_str)
# pythonGPT(latitude_calc, longitude_calc)
# print(f'Celular: {celular}')
# print(f'Modelo: {modelo}')
# print(f'Data: {TEXT_YELLOW} {data}{TEXT_RESET}\nHora: {TEXT_YELLOW}{hora}{TEXT_RESET}')
print(f'{TEXT_YELLOW}={TEXT_RESET}'*60)

# url = f"https://www.google.com/maps/search/{latitude_calc.replace('-', '')} {longitude_calc.replace('-', '')}"
# webbrowser.open_new(url)

# maps_url = f"https://www.google.com/maps?q={latitude_calc.replace('-', '')},{longitude_calc.replace('-', '')}&output=embed"

@st.cache_data
def get_address_opencage(lat, lon):
    # with open(r"C:\Users\Elara\Documents\myAPI.txt", "r") as API_READ:
    # with open(r'C:\Users\steva\exit-project\exif-tool\myAPI.txt', 'r') as API_READ:
        # mykey = API_READ.read()
        # print(f'api key {mykey}')
    # API_KEY = mykey
    api_key = os.gatenv('API')
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    return data['results'][0]['formatted'] if data['results'] else "Endereço não encontrado"

if 'counter' not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1
st.write(f"This page has run {st.session_state.counter} times.")

endereco = get_address_opencage(latitude_test_str, longitude_test_str)
st.title(endereco)
st.write(latitude_calc, longitude_calc)

# Obter a hora atual
now = datetime.now()
current_hour = now.strftime('%H:%M:%S')

match now:
    case n if n.hour < 12:
        st.sidebar.warning(f'🌅 Bom Dia')
    case n if 12 <= n.hour < 18:
        st.sidebar.write("🌞 Boa Tarde!")
    case n if 18 <= n.hour < 22:
        st.sidebar.write("🌜 Boa Noite!")
    case _:
        st.write("🌃 Good night!")

# todayInfo = datetime.today
# print(todayInfo)

# Folium
m = folium.Map(location=[latitude_test_str, longitude_test_str], zoom_start=15)
folium.Marker([latitude_test_str, longitude_test_str], popup="Localização").add_to(m)

# change text color 

# do u prefer purple or green?
# purple = 1 
# green = ?

#                      SIDEBAR
# ================================================
address_details = geoLocator(latitude_test_str, longitude_test_str)

# print(f'{TEXT_GREEN} {current} {TEXT_RESET}')

st.sidebar.title('More infos')
st.sidebar.markdown(textColor(f'Marca e Modelo do celular: {celular.upper()}, {modelo.upper()}', 'green'), unsafe_allow_html=True)
# st.sidebar.write(f'Marca e modelo |{celular.upper()} {modelo.upper()}')
st.sidebar.markdown(textColor(f'Hora: {current_hour}', 'green'),unsafe_allow_html=True )
st.sidebar.markdown(textColor(f'Dia: {data}', 'purple'), unsafe_allow_html=True)


# we have to create a function to get this file using st.file.uploader
st.sidebar.image('img/IMG_20250205_174349.jpg')
# displayTime()
chat = knowMore(latitude_test_str, longitude_test_str)
if st.sidebar.button('Know more'):
    st.sidebar.write(f'Renata:\n  {chat}')

st.sidebar.write(address_details)
st.sidebar.audio('img/90sFlav - Call me.mp3', autoplay=True, loop=True)
# ================================================

# Exibir o mapa no Streamlit
st_data = st_folium(m, width=700, height=500)

weather = getWeather(latitude_test_str,longitude_test_str)
print(weather)