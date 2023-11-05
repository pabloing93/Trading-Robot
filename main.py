from functions import *
import time

cont = 0

while(cont <= 10):
  print(cont)
  history = get_history()
  # print(history)
  df_bitcoin = importar_base_bitcoin()
  datetime = df_bitcoin.index[-1]
  precio, tendencia = extraer_tendencias("BTC")
  media_bitcoin = limpieza_datos(df_bitcoin)
  decision = tomar_desiciones(precio, media_bitcoin, tendencia)
  record = {'Datetime': datetime, 'Price': precio, 'Decision': decision}
  last_history = pandas.DataFrame([record])
  history = pandas.concat([history, last_history], ignore_index=True)
  # print(last_history)
  save_history(history)
  # visualizacion(df_bitcoin, precio, media_bitcoin, decision)
  cont = cont + 1
  time.sleep(60)