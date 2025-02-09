from exif import Image
import requests
import folium
import streamlit as st
from streamlit_folium import st_folium
from datetime import datetime
from Functions.pythonGPT import knowMore
from Functions.textColor import textColor
from Functions.Colors import Colors
TEXT_RED, TEXT_GREEN, TEXT_YELLOW, TEXT_RESET = Colors()
from Functions.todayInfo import displayTime
import os

def upload_image():
    uploaded_file = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        save_dir = "img"
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Imagem salva em: {file_path}")
        st.image(file_path, caption="Imagem carregada")
        
        return file_path
    return None
    
img_path = upload_image()

my_image = None 
if img_path:
    with open(img_path, 'rb') as image_file:
        my_image = Image(image_file.read())
else:
    st.error("Nenhuma imagem foi carregada.") 
    img_path = None

def longitude():
    if not my_image.has_exif:
        st.error("A imagem não contém dados EXIF.")
        return None, None
    
    if not hasattr(my_image, 'gps_longitude') or not hasattr(my_image, 'gps_longitude_ref'):
        return None, None
    longitude_test = my_image.gps_longitude[0] + (my_image.gps_longitude[1] / 60) + (my_image.gps_longitude[2] / 3600)

    if my_image.gps_longitude_ref == "W":
        longitude_test_str = "-" + str(longitude_test)
    else:
        longitude_test_str = str(longitude_test)

    longitude_list_mode = [int(i) for i in longitude_test_str if i.isdigit()]

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

    return longitude_calc, longitude_test_str

def latitude():
    if not my_image.has_exif:
        st.error("A imagem não contém dados EXIF.")
        return None, None
    
    if not hasattr(my_image, 'gps_latitude') or not hasattr(my_image, 'gps_latitude_ref'):
        st.error("A imagem não contém informações de latitude ou longitude.")
        return None, None
    
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
geoLocator(latitude_test_str, longitude_test_str)
print(f'Latitude: {latitude_calc} Longitude: {longitude_calc}')
print(f'{TEXT_YELLOW} PYTHON GPT {TEXT_RESET}')
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
    #     mykey = API_READ.read()
    # API_KEY = mykey 
    API = os.getenv('API')
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={API}"
    response = requests.get(url)
    data = response.json()
    
    return data['results'][0]['formatted'] if data['results'] else "Endereço não encontrado"

# @st.cache_data
# def get_weather(lat, lon):
#     with open(r"C:\Users\Elara\Documents\weatherAPI.txt", "r") as API_READ:
#         weather_key = API_READ.read()
#     API_KEY = weather_key
#     url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
#     response = requests.get(url)
#     data = response.json()
    
#     if data['cod'] == 200:
#         weather_description = data['weather'][0]['description']
#         temperature = data['main']['temp']
#         return f"{weather_description.capitalize()}, {temperature}°C"
#     else:
#         return "Clima não encontrado"

# if 'counter' not in st.session_state:
#     st.session_state.counter = 0


st.session_state.counter += 1
st.write(f"This page has run {st.session_state.counter} times.")

endereco = get_address_opencage(latitude_test_str, longitude_test_str)
st.title(endereco)
st.write(latitude_calc, longitude_calc)

st.sidebar.title('sidebar title')

st.sidebar.write(f'marca e modelo |{celular.upper()} {modelo.upper()}')

# Folium
m = folium.Map(location=[latitude_test_str, longitude_test_str], zoom_start=15)
folium.Marker([latitude_test_str, longitude_test_str], popup="Localização").add_to(m)


st.write(f'Dia: {data}')
st.write(f'Hora: {hora}')
st.write(f'Marca e modelo {celular}, {modelo}')
# Exibir o mapa no Streamlit
st_data = st_folium(m, width=700, height=500)
