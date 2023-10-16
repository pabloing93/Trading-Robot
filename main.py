from functions import *
from IPython.display import clear_output
import time

# cont = 0

while(True):
  clear_output()
  # print(f'REFRESH N°: {cont}\n')
  df_bitcoin = importar_base_bitcoin()
  precio, tendencia = extraer_tendencias("BTC")
  print(f'Precio actual: {precio}\n')
  print(f'Tendencia: {tendencia}\n')
  df_bitcoin, media_bitcoin = limpieza_datos(df_bitcoin)
  decision = tomar_desiciones(precio, media_bitcoin, tendencia)
  print(f'Decición: {decision}\n')
  visualizacion(df_bitcoin, precio, media_bitcoin, decision)
  # cont = cont + 1
  time.sleep(300)