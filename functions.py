import yfinance
from bs4 import BeautifulSoup
import requests
from global_data import user_agent
import pandas
import matplotlib.pyplot as matplot

#Getting Yahoo! Finance Bitcoin History Data
def importar_base_bitcoin():
  bitcoin = yfinance.Ticker("BTC-USD")
  df_bitcoin = bitcoin.history(period="7d", interval="5m")
  return df_bitcoin

#Getting tendencies from CoinMarket
def extraer_tendencias(simbol: str) -> tuple:

  def get_tendencie(row: str) -> str:
    alta_icon = "icon-Caret-up"
    baja_icon = "icon-Caret-down"
    if(alta_icon in row):
      return "alta"
    else:
      return "baja"

  def str_to_float(price: str) -> float:
    return float(price.replace("$", "").replace(",", ""))

  def get_column_position(a_table: BeautifulSoup, column_name: str) -> int:
    for index, columna in enumerate(list(a_table.thead.tr.find_all("th"))):
      if(columna.find('p')):
        texto_p = columna.p.text.strip()
        if column_name == texto_p:
          return index

  def get_simbol_row(a_table: BeautifulSoup, a_simbol: str) -> list:
    for tr in a_table.tbody:
      p_tags = tr.find_all("p")
      for p in p_tags:
        if(p.string == a_simbol):
          return list(tr)
  
  #1) Obtengo el html de la web
  headers = { "User-Agent": user_agent }
  url = "https://coinmarketcap.com/"
  request = requests.get(url, headers)
  web_content = BeautifulSoup(request.content, features="lxml")
  html_table = web_content.find("table", class_="cmc-table")

  #2) obtengo la posicion de las columnas que me interesan
  tendencie_column_position = get_column_position(html_table, "1h %")
  price_column_position = get_column_position(html_table, "Price")

  #3) obtengo la fila de la moneda que me interesa
  simbol_row = get_simbol_row(html_table, simbol)

  #4) Accedo al contenido especifico que busco
  price_string = str(simbol_row[price_column_position].span.text)
  price = str_to_float(price_string) #limpio el dato
  tendencie_string = str(simbol_row[tendencie_column_position])
  tendencie = get_tendencie(tendencie_string) #limpio el dato

  return ( price, tendencie )

def tomar_desiciones(current_price: int, mean_price: int, tendencie: str) -> str:
  case_1 = (current_price >= mean_price) & tendencie == 'baja'
  case_2 = (current_price < mean_price) & tendencie == 'alta'

  if (case_1):
    decision = 'Vender'
  elif (case_2):
    decision = 'Comprar'
  else:
    decision = ""

  return decision 

def visualizacion(dataframe: pandas, mean: float, decision: str):
 #los parámetros funcionan por copia
 dataframe['Promedio'] = mean
 print(dataframe)
 #configurar tamaño 16x5
 #Adicionar un título al gráfico 
 #Usando el método plot() dibujar una línea en el gráfico con los datos de Datetime y Close
 #usando el método plot() dibujar una linea en el grafico con los datos Datetime y Promedio
 #Mostrar la decision con el metodo annotate()
 show()


df_bitcoin = importar_base_bitcoin()
media_bitcoin = 20000.98
decision = 'Comprar'
visualizacion(df_bitcoin, media_bitcoin, decision)