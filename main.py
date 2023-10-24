from functions import *
from IPython.display import clear_output
import time

while(True):
  clear_output()
  df_bitcoin = importar_base_bitcoin()
  precio, tendencia = extraer_tendencias("BTC")
  media_bitcoin = limpieza_datos(df_bitcoin)
  decision = tomar_desiciones(precio, media_bitcoin, tendencia)
  visualizacion(df_bitcoin, precio, media_bitcoin, decision)
  time.sleep(300)