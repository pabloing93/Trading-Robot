from functions import *
from IPython.display import clear_output
import time

while(True):
  clear_output()
  #Con el método importar_base_bitcoin() obtengo un DataFrame desde Yahoo! Finance API
  df_bitcoin = importar_base_bitcoin()
  #Con el método extraer_tendencias() Realizo webscraping para obtener informacion desde coinmarket
  precio, tendencia = extraer_tendencias("BTC")
  #Realizo una limpieza del dataframe de YFinance y obtengo la media
  media_bitcoin = limpieza_datos(df_bitcoin)
  #tomar_decision() me retorna un consejo según el precio actual, la tendencia y el valor de la media
  decision = tomar_desiciones(precio, media_bitcoin, tendencia)
  #visualizacion() muestra los resultados en un gráfico
  visualizacion(df_bitcoin, precio, media_bitcoin, decision)
  print(precio, tendencia, media_bitcoin, decision)
  time.sleep(300)