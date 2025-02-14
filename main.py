from exif import Image
import requests
import folium
import streamlit as st
from streamlit_folium import st_folium
from datetime import datetime
from Functions.getWeather import getWeather
import os


OPENCAGE_API_KEY = "YOUR API KEY HERE"

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

# Pegando a imagem
img_path = upload_image()
my_image = None 
if img_path:
    try:
        with open(img_path, 'rb') as image_file:
            my_image = Image(image_file.read())
    except Exception as e:
        st.error(f"Erro ao carregar a imagem: {e}")
else:
    st.error("Nenhuma imagem foi carregada.")
    st.warning('Adicione uma imagem, por favor.')
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
            st.error("A imagem não contém informações de GPS")
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

if my_image is not None:  
    if not my_image.has_exif:
        st.error("A imagem não contém dados EXIF.")
        st.stop()

if my_image and my_image.has_exif:
    longitude_calc, longitude_test_str = longitude()
    latitude_calc, latitude_test_str = latitude()
    
    if hasattr(my_image, 'datetime_original'):
        horarioDaFoto = my_image.datetime_original
        data, hora = horarioDaFoto.split(' ')
    else:
        horarioDaFoto = "Data não disponível"
        data, hora = "Desconhecido", "Desconhecido"
    
    celular = getattr(my_image, 'make', "Marca não disponível")
    modelo = getattr(my_image, 'model', "Modelo não disponível")      

    # OpenCage API
    if longitude_calc and latitude_calc:
        @st.cache_data
        def get_address_opencage(lat, lon):
            try:
                url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={OPENCAGE_API_KEY}"
                response = requests.get(url)
                data = response.json()
                
                return data['results'][0]['formatted'] if data['results'] else "Endereço não encontrado"
            except Exception as e:
                st.error(f"Erro ao obter o endereço: {e}")

        endereco = get_address_opencage(latitude_test_str, longitude_test_str)
        st.title(endereco)

        # Obter a hora atual
        now = datetime.now()

        match now:
            case n if n.hour < 12:
                st.sidebar.warning(f'🌅 Bom Dia')
            case n if 12 <= n.hour < 18:
                st.sidebar.write("🌞 Boa Tarde!")
            case n if 18 <= n.hour < 22:
                st.sidebar.write("🌜 Boa Noite!")
            case _:
                st.sidebar.write("👋 Ola!")

        # Folium
        m = folium.Map(location=[latitude_test_str, longitude_test_str], zoom_start=15)
        folium.Marker([latitude_test_str, longitude_test_str], popup="Localização").add_to(m)
    
        
        #                      SIDEBAR
        # ================================================
        st.sidebar.markdown('**Informações**')
        st.sidebar.markdown(f'**Marca**: {celular.capitalize()}')
        st.sidebar.markdown(f'**Modelo**: {modelo.title()}')
        st.sidebar.markdown(f"**Latitude**: {latitude_calc}")
        st.sidebar.markdown(f"**Longitude**: {longitude_calc}")

        # Exibir o mapa no Streamlit
        st_data = st_folium(m, width=700, height=500)

        weather = getWeather(latitude_test_str, longitude_test_str)
        
        st.sidebar.write(weather)