# import numpy as np
# import matplotlib as ml
from functions import *

df_bitcoin = importar_base_bitcoin()
# print(df_bitcoin)

precio, tendencia = extraer_tendencias("https://coinmarketcap.com/", "BTC")
# print("precio:", precio)
# print("tendencia:", tendencia)