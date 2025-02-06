import Functions.Colors as Colors
TEXT_RED, TEXT_GREEN, TEXT_YELLOW, TEXT_RESET = Colors()

def locate(lat, lon):
  import requests
  api_key = 'd75cdc25dc703dcbdb6daf83c3a0f474'
  url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
  response = requests.get(url)
  if response.status == 200:
    data = response.json()
    return data
  else:
    return f'{TEXT_RED} Erro ao retorna {TEXT_RESET}'