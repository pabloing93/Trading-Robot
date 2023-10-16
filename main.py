from functions import *
from IPython.display import clear_output
import time

# df_bitcoin = importar_base_bitcoin()
# print(df_bitcoin)


# precio, tendencia = extraer_tendencias("BTC")
# print("precio:", precio)
# print("tendencia:", tendencia)

cont = 0

while(True):
  clear_output()
  print(f'REFRESH N°: {cont}\n')
  df_bitcoin = importar_base_bitcoin()
  precio, tendencia = extraer_tendencias("BTC")
  print(f'Precio actual: {precio}\n')
  print(f'Tendencia: {tendencia}\n')
  # limpieza_datos()
  media = 27000
  decision = tomar_desiciones(precio, media, tendencia)
  print(f'Decición: {decision}\n')
  visualizacion(df_bitcoin, precio, media, decision)
  cont = cont + 1
  time.sleep(1)