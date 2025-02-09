import requests
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("API_WEATHER")
def getWeather(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        wind_speed = data['wind']['speed']
        city_name = data['name']
        return f"Clima: {weather_description}, Temperatura: {temperature}°C, Vento: {wind_speed} m/s, Cidade: {city_name}"
    else:
        print(f"Erro na chamada à API: {response.status_code}")
        print(f"Resposta da API: {response.text}")
        return f"Não foi possível obter informações sobre o clima. {data}"
