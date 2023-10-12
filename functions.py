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
def extraer_tendencias(url, simbol: str) -> tuple:

  def get_status(row: str) -> str:
    alta_icon = "icon-Caret-up"
    baja_icon = "icon-Caret-down"
    if(alta_icon in row):
      return "alta"
    else:
      return "baja"

  def str_to_float(price: str) -> float:
    return float(price.replace("$", "").replace(",", ""))

  headers = { "User-Agent": user_agent }
  request = requests.get(url, headers)
  web_content = BeautifulSoup(request.content, features="lxml")
  table = web_content.find("table", class_="cmc-table")
  btc_row = []
  for tr in table.tbody:
    p_tags = tr.find_all("p")
    for p in p_tags:
      if(p.string == simbol):
        btc_row.append(tr)
  status_icon_column = str(list(btc_row[0])[4])
  table_stringed = io.StringIO(str(table))
  df_table = pandas.read_html(table_stringed)[0]
  df = df_table[["Name", "Price", "1h %"]]
  status = get_status(status_icon_column)
  df_bitcoin_row = df.loc[df["Name"] == "BitcoinBTC"].copy()
  df_bitcoin_row["Status"] = status
  price = str_to_float(str(df_bitcoin_row["Price"][0]))
  return ( price, status )
