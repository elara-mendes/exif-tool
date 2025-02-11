import requests
import streamlit as st


OPENWEATHER_API_KEY = "YOUR API KEY HERE"

@st.cache_data
def getWeather(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=pt'
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        wind_speed = data['wind']['speed']
        city_name = data['name']
        clima = f"**Clima**: {weather_description.title()}"
        Temperatura = f"**Temperatura**: {temperature}°C"
        Vento = f"**Vento**: {wind_speed} m/s"
        Cidade = f"**Cidade**: {city_name}"
        return f"{clima}\n\n{Temperatura}\n\n{Vento}\n\n{Cidade}"
    else:
        print(f"Erro na chamada à API: {response.status_code}")
        print(f"Resposta da API: {response.text}")
        return f"Não foi possível obter informações sobre o clima. Verifique a chave API."
