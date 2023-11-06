from functions import *
import time

# Getting de histories
history = get_history('decision_history')
relevant_history = get_history('relevant_history')
count = 0

# records = [
#   {'Datetime':'2023-11-06 23:00:00+0000', 'Price': 35052.68, 'Decision': 'Comprar'},
#   {'Datetime':'2023-11-06 00:00:00+0000', 'Price': 35052.68, 'Decision': 'Comprar'},
#   {'Datetime':'2023-11-06 00:00:00+0000', 'Price': 35052.68, 'Decision': 'Comprar'},
#   {'Datetime':'2023-11-06 23:00:00+0000', 'Price': 35052.68, 'Decision': 'Vender'},
#   {'Datetime':'2023-11-06 00:00:00+0000', 'Price': 35052.68, 'Decision': 'Esperar'},
#   {'Datetime':'2023-11-06 00:00:00+0000', 'Price': 35052.68, 'Decision': 'Esperar'},
#   {'Datetime':'2023-11-06 00:00:00+0000', 'Price': 35052.68, 'Decision': 'Esperar'},
#   {'Datetime':'2023-11-06 00:00:00+0000', 'Price': 35052.68, 'Decision': 'Esperar'},
#   {'Datetime':'2023-11-06 00:00:00+0000', 'Price': 35052.68, 'Decision': 'Vender'},
#   {'Datetime':'2023-11-06 23:00:00+0000', 'Price': 35052.68, 'Decision': 'Comprar'},
#   {'Datetime':'2023-11-06 00:00:00+0000', 'Price': 35052.68, 'Decision': 'Comprar'}
# ]

# for record in records:
#   print(record)
#   df_record = pandas.DataFrame([record])
#   history = pandas.concat([history, df_record], ignore_index=True)
#   criterio = (record['Decision'] != 'Esperar') & (record['Decision'] != relevant_history.iloc[-1]['Decision'])
#   if (criterio):
#     relevant_history = pandas.concat([relevant_history, df_record], ignore_index=True)

# print('Terminó bucle')
# save_history(history, 'decision_history')
# save_history(relevant_history, 'relevant_history')



while(count <= 30):
  # Execute the bot decisions
  print(count)
  df_bitcoin = importar_base_bitcoin()
  # print(df_bitcoin)
  precio, tendencia = extraer_tendencias("BTC")
  media_bitcoin = limpieza_datos(df_bitcoin)
  decision = tomar_desiciones(precio, media_bitcoin, tendencia)
  #create the record
  datetime = df_bitcoin.index[-1]
  record = {'Datetime': datetime, 'Price': precio, 'Decision': decision}
  print(record)
  df_record = pandas.DataFrame([record])
  history = pandas.concat([history, df_record], ignore_index=True)
  criterio = (record['Decision'] != 'Esperar') & (decision != relevant_history.iloc[-1]['Decision'])
  if (criterio):
    relevant_history = pandas.concat([relevant_history, df_record], ignore_index=True)
  #Add the record and repeat
  # add_record(record, history)
  count = count + 1
  time.sleep(60)

print('Terminó bucle')
save_history(history, 'decision_history')
save_history(relevant_history, 'relevant_history')

