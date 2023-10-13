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
