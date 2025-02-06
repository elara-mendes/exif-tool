import imageio.v3 as iio
from datetime import timezone, datetime
import json
import Functions.Colors as Colors
TEXT_RED, TEXT_GREEN, TEXT_YELLOW, TEXT_RESET = Colors()


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
