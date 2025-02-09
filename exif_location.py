from exif import Image
import requests
import folium
import streamlit as st
from streamlit_folium import st_folium
from datetime import datetime
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
    
    return latitude_calc, latitude_test_str

@st.cache_data
def get_address_opencage(lat, lon):
    with open(r"C:\Users\Elara\Documents\myAPI.txt", "r") as API_READ:
    # with open(r'C:\Users\steva\exit-project\exif-tool\myAPI.txt', 'r') as API_READ:
        mykey = API_READ.read()
        print(f'api key {mykey}')
    API_KEY = mykey
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    return data['results'][0]['formatted'] if data['results'] else "Endereço não encontrado"

if my_image and my_image.has_exif:
    latitude_calc, latitude_test_str = latitude()
    longitude_calc, longitude_test_str = longitude()

    

    # Folium
    if latitude_test_str and longitude_test_str:
        endereco = get_address_opencage(latitude_test_str, longitude_test_str)
        st.title(endereco)
        
        try:
            latitude_test_float = float(latitude_test_str)
            longitude_test_float = float(longitude_test_str)
            
            if -90 <= latitude_test_float <= 90 and -180 <= longitude_test_float <= 180:
                m = folium.Map(location=[latitude_test_float, longitude_test_float], zoom_start=15)
                folium.Marker([latitude_test_float, longitude_test_float], popup="Localização").add_to(m)
                st_data = st_folium(m, width=700, height=500)
            else:
                st.error("A latitude ou longitude estão fora dos limites válidos.")
        except ValueError:
            st.error("Latitude ou Longitude não são valores válidos para criar o mapa.")
    else:
        st.error("Não foi possível obter a latitude ou longitude.")
    
    horarioDaFoto = str(my_image.datetime_original)
    horaFormatada = horarioDaFoto.replace(':','/')
    data, hora = horarioDaFoto.split(' ')
    
    if hasattr(my_image, 'make'):
        celular = str(my_image.make)
    else:
        celular = "Marca não disponível"

    if hasattr(my_image, 'model'):
        modelo = str(my_image.model)
    else:
        modelo = "Modelo não disponível"
        
    new_data = datetime.strptime(data, "%Y:%m:%d")
    new_data_obj = new_data.strftime("%d/%m/%Y")
    
    # Informações
    st.write(f'Latitude: {latitude_calc}')
    st.write(f'Longitude: {longitude_calc}')
    st.write(f'Data: {new_data_obj}')
    st.write(f'Hora: {hora}')
    st.write(f'Marca: {celular.capitalize()}')
    st.write(f'Modelo: {modelo.title()}')
