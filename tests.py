# import numpy as np
# import matplotlib as ml
from functions import *
import pandas

df_bitcoin = importar_base_bitcoin()
# precio, tendencia = extraer_tendencias("BTC")

# df_bitcoin.info()
data_types = pandas.DataFrame(df_bitcoin.dtypes, columns = ['Tipo de dato'])
data_types.columns.name = "Columna"
tabla_bitcoin = pandas.read_html("https://coinmarketcap.com/")[0]
tabla_bitcoin_columnas = list(tabla_bitcoin.columns)
columnas_interes = [ "Name", "Price", "1h %" ]
columnas_posicion = []
for index, columna in enumerate(tabla_bitcoin_columnas):
  for columna_interes in columnas_interes:
    if columna_interes == columna:
      columnas_posicion.append({"nombre": columna, "pos": index})

for objeto in columnas_posicion:
  print(objeto['nombre'])


# ¿cómo puedo determinar si hay duSplicados en una columna?
# cuando determine si hay duplicados ¿cómo elimino duplicados de una columna?
# ¿cómo elimino valores nulos?
# ¿como podría determinar todos los registros cuyo valor en volumen es = 0?
# ¿cómo detectar la cantidad de registros?

# Eliminar duplicados de la columna DateTime
# Eliminar registros cuyo volumen de operacion = 0
# Eliminar registros nulos de la columna Close
