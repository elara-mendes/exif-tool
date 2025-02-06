# pip install imageio
import imageio.v3 as iio
import exifread as ex
from datetime import timezone, datetime
import json

caminho_imagem = '/img/C:\Users\steva\exit-project\exif-tool\img\modo serio - Search Images e mais 3 páginas - Pessoal — Microsoft​ Edge 05_02_2025 14_51_48.PNG'
another_img = 'img\modo serio - Search Images e mais 3 páginas - Pessoal — Microsoft​ Edge 05_02_2025 14_51_48.PNG'

def Colors():
  TEXT_RED = '\033[31m'
  TEXT_GREEN = '\033[32m'
  TEXT_YELLOW = '\033[33m'
  TEXT_RESET = '\033[0m'
  return TEXT_RED, TEXT_GREEN, TEXT_YELLOW, TEXT_RESET

TEXT_RED, TEXT_GREEN, TEXT_YELLOW, TEXT_RESET = Colors()

def getLocate(img):
  with open(img, 'rb') as f:
    tags = ex.process_file(f)
    print(f'array length: {len(tags)}')
    print(f'data: {tags}')  


    try:
      latitude = tags["GPS GPSLatitude"]
      longitude = tags["GPS GPSLongitude"]

      # locate(latitude, longitude)
      # return latitude, longitude
    except KeyError:
      return f'{TEXT_RED}Não foi possível encontrar localização {TEXT_RESET}'


def read_data(img):
  meta = iio.immeta(img)
  game_dvr_extended = meta.get('Microsoft.GameDVR.Extended')
  
  mode = meta.get('shape')
  width, height = mode[1], mode[0]
  print(f'{TEXT_RED} Colunas {width} e Linhas {height} {TEXT_RESET} \n')
  
  game_dvr_title = meta.get('Microsoft.GameDVR.Title')  
  print(f"Nome da Foto: {game_dvr_title}")
  
  if game_dvr_extended:
    game_dvr_data = json.loads(game_dvr_extended)
    id = game_dvr_data.get('localId')  
    start_time = game_dvr_data.get('startTime')  

    horarioDaFoto = game_dvr_data.get('startTime')
    data = horarioDaFoto[0:10]
    print(f'data {data}')
    horarioDaFoto = datetime.fromisoformat(horarioDaFoto).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Horário da Foto: {TEXT_GREEN} {horarioDaFoto} {TEXT_RESET}")
    
    print(f"Localização: {getLocate(img)}")

    print(f'Local ID: {id}')

    print('='*30)

    # getLocate(img)
  else:
    print("Erro ao ler dados")


read_data(another_img)
getLocate(another_img)

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