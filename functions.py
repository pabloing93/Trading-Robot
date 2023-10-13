import yfinance
from bs4 import BeautifulSoup
import requests
from global_data import user_agent
import pandas
import io

#Getting Yahoo! Finance Bitcoin History Data
def importar_base_bitcoin():
  bitcoin = yfinance.Ticker("BTC-USD")
  df_bitcoin = bitcoin.history(period="7d", interval="5m")
  return df_bitcoin

#Getting tendencies from CoinMarket
def extraer_tendencias(simbol: str) -> tuple:

  def get_status(row: str) -> str:
    alta_icon = "icon-Caret-up"
    baja_icon = "icon-Caret-down"
    if(alta_icon in row):
      return "alta"
    else:
      return "baja"

  def str_to_float(price: str) -> float:
    return float(price.replace("$", "").replace(",", ""))

  #1) Obtengo el html de la web
  headers = { "User-Agent": user_agent }
  url = "https://coinmarketcap.com/"
  request = requests.get(url, headers)
  web_content = BeautifulSoup(request.content, features="lxml")
  table = web_content.find("table", class_="cmc-table")

  #2) obtengo la tabla para acceder al nombre de las columnas que me interesan y su posición
  columnas_interes = [ "Name", "Price", "1h %" ]
  position = {}
  for index, columna in enumerate(list(table.thead.tr.find_all("th"))):
    if(columna.find('p')):
      texto_p = columna.p.text.strip()
      for columna_interes in columnas_interes:
        if columna_interes == texto_p:
          position[texto_p] = index

  #3) obtengo la fila de la moneda que me interesa
  btc_row = []
  for tr in table.tbody:
    p_tags = tr.find_all("p")
    for p in p_tags:
      if(p.string == simbol):
        btc_row.append(tr)

  # name = list(btc_row[0])[position['Name']].p.text
  #4) busco en la fila de la moneda los valores de las columnas que me interesan accediendo a su posicion ya conocida
  price_string = str(list(btc_row[0])[position['Price']].span.text) #acá obtengo el valor del precio y lo conviero en string
  price = str_to_float(price_string)
  status_icon_column = str(list(btc_row[0])[position['1h %']]) #de esta fila me interesa el row completo y lo convierto en string
  status = get_status(status_icon_column)

  return ( price, status )
