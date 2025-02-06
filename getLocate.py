import Colors
import exifread as ex
TEXT_RED, TEXT_GREEN, TEXT_YELLOW, TEXT_RESET = Colors()


def getLocate(img):
  with open(img, 'rb') as f:
    tags = ex.process_file(f)
    print(f'array length: {len(tags)}')
    print(f'data: {tags}')


    try:
      latitude = tags["GPS GPSLatitude"]
      longitude = tags["GPS GPSLongitude"]
      locate(latitude, longitude)
      # return latitude, longitude
    except KeyError:
      return f'{TEXT_RED}Não foi possível encontrar localização {TEXT_RESET}'
