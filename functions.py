import yfinance
from bs4 import BeautifulSoup
import requests
from global_data import user_agent
import pandas
import matplotlib.pyplot as plt
import os

def continues():
  input('Presione ENTER para continuar')
  os.system('powershell clear-host')

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

def limpieza_datos(df_bitcoins: pandas.DataFrame) -> tuple:
  def draw_boxplot(title: str, dataframe: pandas):
    plt.figure(figsize=(8, 6))
    plt.title(title)
    plt.boxplot(dataframe['Close'], vert=False)
    plt.show()
  
  # Hago una copia del dataframe original
  dataframe = df_bitcoins.copy()

  # Eliminar duplicados en el índice
  dataframe = dataframe[~dataframe.index.duplicated(keep='first')]
  
  # Buscar valores nulos en la columna "Close" y eliminarlos
  dataframe.dropna(subset=['Close'], inplace=True)
  
  # Verificar que todos los registros tengan un Volume de transacción mayor a 0
  dataframe = dataframe[dataframe['Volume'] > 0]
  
  # Identificar y eliminar outliers en la columna "Close" usando un boxplot
  
  #Obtengo los valores de Close que se encuentren entre Q1 y Q3
  Q1 = dataframe['Close'].quantile(0.25)
  Q3 = dataframe['Close'].quantile(0.75)
  dataframe = dataframe[(dataframe['Close'] >= Q1) & (dataframe['Close'] <= Q3)]

  # Calcular el precio promedio (Close) de esta selección
  media_bitcoin = dataframe['Close'].mean()
  return media_bitcoin

def tomar_desiciones(current_price: int, mean_price: int, tendencie: str) -> str:

  #Defino los casos de decisiones
  case_1 = (current_price >= mean_price) & (tendencie == 'baja')
  case_2 = (current_price < mean_price) & (tendencie == 'alta')

  if (case_1):
    decision = 'Vender'
  elif (case_2):
    decision = 'Comprar'
  else:
    decision = 'Esperar'
  return decision 

def visualizacion(df_bitcoin: pandas, current_price: float, mean: float, decision: str):

  #Hago una copia del DF original
  dataframe = df_bitcoin.copy()
  #Creo una columna nueva y cargo el valor de la media
  dataframe['Promedio'] = mean
  #Configuro el tamaño del gráfico en 16x5
  plt.rc('figure', figsize = (16,5))
  #Dibujo el gráfico (Volumen,Datetime)
  graph = dataframe['Close'].plot()
  #Dibujo la linea del promedio
  graph = dataframe['Promedio'].plot()
  #Seteo títulos al gráfico 
  graph.set_title('Bitcoin BTC YFinance', {'fontsize': 22})
  graph.set_ylabel('Precio de Cierre')
  graph.set_xlabel('Fecha')
  #Mostrar la decision con el metodo annotate()
  current_date = dataframe.index[-1]
  if (decision == 'Comprar'):
    plt.annotate(
      text = decision, 
      horizontalalignment = 'center',
      xy=(current_date, current_price),
      arrowprops={'facecolor': 'green'},
      xytext=(current_date, current_price+100)
    ) 
  elif (decision == 'Vender'):
    plt.annotate(
      text = decision,
      horizontalalignment = 'center',
      xy=(current_date, current_price), 
      arrowprops={'facecolor': 'red'},
      xytext=(current_date, current_price+500)
    )
  graph.legend(
    [f'Bitcoin Price: {round(current_price, 2)}', f'Mean: {round(mean, 2)}'], 
    loc='upper left',
    title=f'Recomendacion: {decision}')
  plt.show()