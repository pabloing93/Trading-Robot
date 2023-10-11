import yfinance
from bs4 import BeautifulSoup
import requests
from global_data import user_agent

def example(number):
  return number * 2

#Getting Yahoo! Finance Bitcoin History Data
def get_yf_data():
  btc = yfinance.Ticker("BTC-USD")
  df_btc = btc.history(period="7d", interval="5m")
  return df_btc

#Getting tendencies from CoinMarket
def get_tendencies(url):
  headers = { "User-Agent": user_agent }
  request = requests.get(url, headers)
  web_content = BeautifulSoup(request.content, features="lxml")
  x = web_content.findAll("div", {"class": "class_name"})
  return x


# print(get_yf_data())
print(get_tendencies("https://coinmarketcap.com/"))