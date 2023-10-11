import yfinance
from bs4 import BeautifulSoup
import requests
from global_data import user_agent

def example(number):
  return number * 2

#Getting Yahoo! Finance Bitcoin History Data
def importar_base_bitcoin():
  bitcoin = yfinance.Ticker("BTC-USD")
  df_bitcoin = bitcoin.history(period="7d", interval="5m")
  return df_bitcoin

#Getting tendencies from CoinMarket
def extraer_tendencias(url):
  headers = { "User-Agent": user_agent }
  request = requests.get(url, headers)
  web_content = BeautifulSoup(request.content, features="lxml")
  x = web_content.table.tbody.tr
  precio_actual = float(str(x.find("a", href="/currencies/bitcoin/#markets").span.string).replace('$', '').replace(',', ''))


# print(get_yf_data())
extraer_tendencias("https://coinmarketcap.com/")