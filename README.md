1) pip install pandas, matplotlib, numpy, yfinance, beautifulsoup4, ipython
2) Update user_agent in global.py

How to make a pull
1) git pull origin dev

Github commands
How to make a Push
1) git add .
2) git commit -m "commit name"
3) git push origin dev
# Trading Robot 🤖

## Configuracion del ambiente 📊

BeautifulSoup (bs4)
BeautifulSoup, o bs4, es una biblioteca utilizada para analizar y extraer información de páginas web en formato HTML y XML. Para instalarlo, puedes usar:

Numpy
Numpy es una biblioteca fundamental para el procesamiento numérico en Python. Aunque no se mencionó en la descripción original, es una biblioteca comúnmente utilizada en proyectos de análisis de datos y finanzas. 

Pandas
pandas es una biblioteca esencial para el análisis y manipulación de datos en Python. Se utiliza ampliamente en proyectos de análisis de datos financieros. 

Matplotlib
Matplotlib es una biblioteca de visualización de datos en Python, y pyplot es un módulo de matplotlib que permite crear gráficos y visualizaciones. 

```python
import yfinance
from bs4 import BeautifulSoup
import requests
from global_data import user_agent
import pandas
import matplotlib.pyplot as plt
from datetime import datetime
```


## Obtencion de datos 📁

La función importar_base_bitcoin utiliza yfinance para obtener datos históricos de Bitcoin durante los últimos 7 días con intervalos de 5 minutos.

```python
def importar_base_bitcoin():
  bitcoin = yfinance.Ticker("BTC-USD")
  df_bitcoin = bitcoin.history(period="7d", interval="1m")
  return df_bitcoin
```
La función extraer_tendencias toma el nombre de la criptomoneda que te interesa, como "Bitcoin" (esto es el "símbolo"), y luego realiza las siguientes acciones:

Examina una página web que muestra datos sobre muchas criptomonedas.
Encuentra la columna que muestra cómo ha cambiado el precio de Bitcoin en la última hora (si ha subido o bajado).
Busca la fila que corresponde a Bitcoin en la tabla de datos.
Luego, extrae la información sobre el precio y si está subiendo o bajando.
Al final, la función te proporciona dos cosas: el precio actual de Bitcoin y si su precio ha estado subiendo o bajando recientemente.

```python
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
```


## Limpieza de datos🧹

Aquí hay una descripción de lo que hace:

- Comienza haciendo una copia de los datos originales de Bitcoin para no modificar los datos originales directamente.
- Elimina cualquier fila duplicada en los datos basándose en el índice de tiempo.
- Elimina las filas que contienen valores nulos (información faltante) en la columna que muestra el precio de cierre ("Close").
- Filtra las filas para asegurarse de que todas tengan un volumen de transacción mayor a cero. Esto es importante para eliminar datos que no son útiles.
- Identifica y elimina valores inusuales o "outliers" en el precio de cierre de Bitcoin utilizando un gráfico de caja (boxplot). Los outliers son valores muy por encima o por debajo del promedio y se eliminan para obtener datos más precisos.
- Calcula el precio promedio (o media) de cierre de Bitcoin basado en los datos limpios y actualizados.




```python
def limpieza_datos(df_bitcoins: pandas) -> tuple:

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
  # draw_boxplot('Boxplot de la columna "Close"', dataframe) #Método para graficar el boxplot
  
  #Obtengo los valores de Close que se encuentren entre Q1 y Q3
  Q1 = dataframe['Close'].quantile(0.25)
  Q3 = dataframe['Close'].quantile(0.75)
  dataframe = dataframe[(dataframe['Close'] >= Q1) & (dataframe['Close'] <= Q3)]
  
  # draw_boxplot('Boxplot actualizado', dataframe) #Método para graficar el boxplot
  
  # Calcular el precio promedio (Close) de esta selección
  media_bitcoin = dataframe['Close'].mean()

  return media_bitcoin
```
En resumen, este código se encarga de asegurarse de que los datos relacionados con el precio de Bitcoin sean precisos y útiles para futuros análisis. Esto implica eliminar datos duplicados, nulos e inusuales, y calcular el precio promedio después de realizar estas limpiezas.

## Toma de decisiones 🚀


Aquí está una descripción de lo que hace esta función:

- La función toma tres valores como entrada: el precio actual (`current_price`), el precio promedio (`mean_price`), y la tendencia (`tendencie`) que puede ser "alta" o "baja".
- Luego, la función verifica dos casos:
  - Caso 1: Si el precio actual es mayor o igual al precio promedio y la tendencia es "baja", entonces la función decide "Vender".
  - Caso 2: Si el precio actual es menor que el precio promedio y la tendencia es "alta", entonces la función decide "Comprar".
- Si ninguno de estos casos se cumple, la función toma la decisión de "Esperar".
- Finalmente, la función devuelve una decisión, que puede ser "Vender", "Comprar" o "Esperar" en función de los valores de entrada.

Esta función se utiliza para tomar decisiones sobre si comprar, vender o esperar en función de la comparación entre el precio actual, el precio promedio y la tendencia del mercado.


```python
def tomar_desiciones(current_price: int, mean_price: int, tendencie: str) -> str:
  case_1 = (current_price >= mean_price) & (tendencie == 'baja')
  case_2 = (current_price < mean_price) & (tendencie == 'alta')

  if (case_1):
    decision = 'Vender'
  elif (case_2):
    decision = 'Comprar'
  else:
    decision = None

  return decision 
```



## Visualizacion 📈

Aquí está una descripción de lo que hace esta función:

- La función toma varios parámetros como entrada: un DataFrame de pandas (`dataframe`) que contiene datos, el precio actual (`current_price`), el precio promedio (`mean`) y una decisión (`decision`) que puede ser "Comprar", "Vender" o "Esperar".
- La función comienza agregando una nueva columna al DataFrame llamada "Promedio" y asigna el valor del precio promedio a esta columna.
- Configura el tamaño del gráfico en 16x5, lo que determina las dimensiones del gráfico que se va a generar.
- Utiliza el método `plot()` para dibujar una línea en el gráfico con los datos de tiempo ("Datetime") y el precio de cierre ("Close") del DataFrame.
- Luego, utiliza nuevamente el método `plot()` para dibujar una línea en el gráfico con los datos de tiempo y el precio promedio.
- Agrega un título al gráfico que se llama "Bitcoin BTC YFinance" y ajusta el tamaño del título.
- Agrega etiquetas al eje vertical del gráfico para indicar "Precio de Cierre".
- Finalmente, la función muestra el gráfico y, si la decisión es "Comprar" o "Vender", agrega una anotación en el gráfico para mostrar esta decisión en función del precio actual.

Esta función se utiliza para visualizar los datos del precio de Bitcoin en un gráfico, lo que puede ayudar a los usuarios a tomar decisiones basadas en la información presentada en el gráfico, como comprar o vender Bitcoin.


```python
def visualizacion(dataframe: pandas, current_price: float, mean: float, decision: str):
  #los parámetros funcionan por copia
  dataframe['Promedio'] = mean
  #  print(dataframe.describe())
  #configurar tamaño 16x5
  plt.rc('figure', figsize = (16,5))
  #Usando el método plot() dibujar una línea en el gráfico con los datos de Datetime y Close
  graph = dataframe['Close'].plot()
  #usando el método plot() dibujar una linea en el grafico con los datos Datetime y Promedio
  graph = dataframe['Promedio'].plot()
  #Adicionar un título al gráfico 
  graph.set_title('Bitcoin BTC YFinance', {'fontsize': 22})
  graph.set_ylabel('Precio de Cierre')
  #Mostrar la decision con el metodo annotate()
  current_date = dataframe.index[-1]
  if (decision == 'Comprar'):
    plt.annotate(
      text = decision, 
      horizontalalignment = 'center',
      xy=(current_date, current_price), 
      arrowprops={'facecolor': 'green'},
      xytext=(current_date, current_price-100)
    ) 
  elif (decision == 'Vender'):
    plt.annotate(
      text = decision,
      horizontalalignment = 'center',
      xy=(current_date, current_price), 
      arrowprops={'facecolor': 'red'},
      xytext=(current_date, current_price+70)
    )
  plt.show()
```


## Automatizacion 🧠

Automatización del Proceso:

- El código proporcionado se utiliza para automatizar el proceso de seguimiento del precio de Bitcoin y tomar decisiones basadas en ese precio y en su tendencia.
- Se utiliza un bucle `while(True)` para que el proceso se ejecute continuamente.
- En cada iteración del bucle, se muestra un contador de actualizaciones con `print` para mantener un registro de las actualizaciones.
- Luego, se obtiene el precio actual de Bitcoin y su tendencia utilizando las funciones `importar_base_bitcoin` y `extraer_tendencias`.
- Se muestra el precio actual y la tendencia para informar al usuario.
- A continuación, se define un valor objetivo para el precio promedio, que en este caso es de $27,000.
- Utilizando la función `tomar_desiciones`, se toma una decisión basada en el precio actual, el valor objetivo y la tendencia. La decisión puede ser "Comprar", "Vender" o "Esperar".
- Se muestra la decisión al usuario con `print`.
- Finalmente, se utiliza la función `visualizacion` para mostrar un gráfico que incluye el precio actual, el precio promedio y la decisión en tiempo real.
- El bucle continúa ejecutándose, actualizando la información y tomando decisiones a intervalos de 1 segundo.

Este proceso automatizado permite a los usuarios rastrear el precio de Bitcoin y tomar decisiones rápidas basadas en datos actualizados en tiempo real.


```python
cont = 0

while(True):
  clear_output()
  print(f'REFRESH N°: {cont}\n')
  df_bitcoin = importar_base_bitcoin()
  precio, tendencia = extraer_tendencias("BTC")
  print(f'Precio actual: {precio}\n')
  print(f'Tendencia: {tendencia}\n')
  # limpieza_datos()
  media = 27000
  decision = tomar_desiciones(precio, media, tendencia)
  print(f'Decición: {decision}\n')
  visualizacion(df_bitcoin, precio, media, decision)
  cont = cont + 1
  time.sleep(1)
```
# Trading Robot 🤖

## Configuracion del ambiente 📊

BeautifulSoup (bs4)
BeautifulSoup, o bs4, es una biblioteca utilizada para analizar y extraer información de páginas web en formato HTML y XML. Para instalarlo, puedes usar:

Numpy
Numpy es una biblioteca fundamental para el procesamiento numérico en Python. Aunque no se mencionó en la descripción original, es una biblioteca comúnmente utilizada en proyectos de análisis de datos y finanzas. 

Pandas
pandas es una biblioteca esencial para el análisis y manipulación de datos en Python. Se utiliza ampliamente en proyectos de análisis de datos financieros. 

Matplotlib
Matplotlib es una biblioteca de visualización de datos en Python, y pyplot es un módulo de matplotlib que permite crear gráficos y visualizaciones. 

```python
import yfinance
from bs4 import BeautifulSoup
import requests
from global_data import user_agent
import pandas
import matplotlib.pyplot as plt
from datetime import datetime
```


## Obtencion de datos 📁

La función importar_base_bitcoin utiliza yfinance para obtener datos históricos de Bitcoin durante los últimos 7 días con intervalos de 5 minutos.

```python
def importar_base_bitcoin():
  bitcoin = yfinance.Ticker("BTC-USD")
  df_bitcoin = bitcoin.history(period="7d", interval="1m")
  return df_bitcoin
```
La función extraer_tendencias toma el nombre de la criptomoneda que te interesa, como "Bitcoin" (esto es el "símbolo"), y luego realiza las siguientes acciones:

Examina una página web que muestra datos sobre muchas criptomonedas.
Encuentra la columna que muestra cómo ha cambiado el precio de Bitcoin en la última hora (si ha subido o bajado).
Busca la fila que corresponde a Bitcoin en la tabla de datos.
Luego, extrae la información sobre el precio y si está subiendo o bajando.
Al final, la función te proporciona dos cosas: el precio actual de Bitcoin y si su precio ha estado subiendo o bajando recientemente.

```python
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
```


## Limpieza de datos🧹

Aquí hay una descripción de lo que hace:

- Comienza haciendo una copia de los datos originales de Bitcoin para no modificar los datos originales directamente.
- Elimina cualquier fila duplicada en los datos basándose en el índice de tiempo.
- Elimina las filas que contienen valores nulos (información faltante) en la columna que muestra el precio de cierre ("Close").
- Filtra las filas para asegurarse de que todas tengan un volumen de transacción mayor a cero. Esto es importante para eliminar datos que no son útiles.
- Identifica y elimina valores inusuales o "outliers" en el precio de cierre de Bitcoin utilizando un gráfico de caja (boxplot). Los outliers son valores muy por encima o por debajo del promedio y se eliminan para obtener datos más precisos.
- Calcula el precio promedio (o media) de cierre de Bitcoin basado en los datos limpios y actualizados.




```python
def limpieza_datos(df_bitcoins: pandas) -> tuple:

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
  # draw_boxplot('Boxplot de la columna "Close"', dataframe) #Método para graficar el boxplot
  
  #Obtengo los valores de Close que se encuentren entre Q1 y Q3
  Q1 = dataframe['Close'].quantile(0.25)
  Q3 = dataframe['Close'].quantile(0.75)
  dataframe = dataframe[(dataframe['Close'] >= Q1) & (dataframe['Close'] <= Q3)]
  
  # draw_boxplot('Boxplot actualizado', dataframe) #Método para graficar el boxplot
  
  # Calcular el precio promedio (Close) de esta selección
  media_bitcoin = dataframe['Close'].mean()

  return media_bitcoin
```
En resumen, este código se encarga de asegurarse de que los datos relacionados con el precio de Bitcoin sean precisos y útiles para futuros análisis. Esto implica eliminar datos duplicados, nulos e inusuales, y calcular el precio promedio después de realizar estas limpiezas.

## Toma de decisiones 🚀


Aquí está una descripción de lo que hace esta función:

- La función toma tres valores como entrada: el precio actual (`current_price`), el precio promedio (`mean_price`), y la tendencia (`tendencie`) que puede ser "alta" o "baja".
- Luego, la función verifica dos casos:
  - Caso 1: Si el precio actual es mayor o igual al precio promedio y la tendencia es "baja", entonces la función decide "Vender".
  - Caso 2: Si el precio actual es menor que el precio promedio y la tendencia es "alta", entonces la función decide "Comprar".
- Si ninguno de estos casos se cumple, la función toma la decisión de "Esperar".
- Finalmente, la función devuelve una decisión, que puede ser "Vender", "Comprar" o "Esperar" en función de los valores de entrada.

Esta función se utiliza para tomar decisiones sobre si comprar, vender o esperar en función de la comparación entre el precio actual, el precio promedio y la tendencia del mercado.


```python
def tomar_desiciones(current_price: int, mean_price: int, tendencie: str) -> str:
  case_1 = (current_price >= mean_price) & (tendencie == 'baja')
  case_2 = (current_price < mean_price) & (tendencie == 'alta')

  if (case_1):
    decision = 'Vender'
  elif (case_2):
    decision = 'Comprar'
  else:
    decision = None

  return decision 
```



## Visualizacion 📈

Aquí está una descripción de lo que hace esta función:

- La función toma varios parámetros como entrada: un DataFrame de pandas (`dataframe`) que contiene datos, el precio actual (`current_price`), el precio promedio (`mean`) y una decisión (`decision`) que puede ser "Comprar", "Vender" o "Esperar".
- La función comienza agregando una nueva columna al DataFrame llamada "Promedio" y asigna el valor del precio promedio a esta columna.
- Configura el tamaño del gráfico en 16x5, lo que determina las dimensiones del gráfico que se va a generar.
- Utiliza el método `plot()` para dibujar una línea en el gráfico con los datos de tiempo ("Datetime") y el precio de cierre ("Close") del DataFrame.
- Luego, utiliza nuevamente el método `plot()` para dibujar una línea en el gráfico con los datos de tiempo y el precio promedio.
- Agrega un título al gráfico que se llama "Bitcoin BTC YFinance" y ajusta el tamaño del título.
- Agrega etiquetas al eje vertical del gráfico para indicar "Precio de Cierre".
- Finalmente, la función muestra el gráfico y, si la decisión es "Comprar" o "Vender", agrega una anotación en el gráfico para mostrar esta decisión en función del precio actual.

Esta función se utiliza para visualizar los datos del precio de Bitcoin en un gráfico, lo que puede ayudar a los usuarios a tomar decisiones basadas en la información presentada en el gráfico, como comprar o vender Bitcoin.


```python
def visualizacion(dataframe: pandas, current_price: float, mean: float, decision: str):
  #los parámetros funcionan por copia
  dataframe['Promedio'] = mean
  #  print(dataframe.describe())
  #configurar tamaño 16x5
  plt.rc('figure', figsize = (16,5))
  #Usando el método plot() dibujar una línea en el gráfico con los datos de Datetime y Close
  graph = dataframe['Close'].plot()
  #usando el método plot() dibujar una linea en el grafico con los datos Datetime y Promedio
  graph = dataframe['Promedio'].plot()
  #Adicionar un título al gráfico 
  graph.set_title('Bitcoin BTC YFinance', {'fontsize': 22})
  graph.set_ylabel('Precio de Cierre')
  #Mostrar la decision con el metodo annotate()
  current_date = dataframe.index[-1]
  if (decision == 'Comprar'):
    plt.annotate(
      text = decision, 
      horizontalalignment = 'center',
      xy=(current_date, current_price), 
      arrowprops={'facecolor': 'green'},
      xytext=(current_date, current_price-100)
    ) 
  elif (decision == 'Vender'):
    plt.annotate(
      text = decision,
      horizontalalignment = 'center',
      xy=(current_date, current_price), 
      arrowprops={'facecolor': 'red'},
      xytext=(current_date, current_price+70)
    )
  plt.show()
```


## Automatizacion 🧠

Automatización del Proceso:

- El código proporcionado se utiliza para automatizar el proceso de seguimiento del precio de Bitcoin y tomar decisiones basadas en ese precio y en su tendencia.
- Se utiliza un bucle `while(True)` para que el proceso se ejecute continuamente.
- En cada iteración del bucle, se muestra un contador de actualizaciones con `print` para mantener un registro de las actualizaciones.
- Luego, se obtiene el precio actual de Bitcoin y su tendencia utilizando las funciones `importar_base_bitcoin` y `extraer_tendencias`.
- Se muestra el precio actual y la tendencia para informar al usuario.
- A continuación, se define un valor objetivo para el precio promedio, que en este caso es de $27,000.
- Utilizando la función `tomar_desiciones`, se toma una decisión basada en el precio actual, el valor objetivo y la tendencia. La decisión puede ser "Comprar", "Vender" o "Esperar".
- Se muestra la decisión al usuario con `print`.
- Finalmente, se utiliza la función `visualizacion` para mostrar un gráfico que incluye el precio actual, el precio promedio y la decisión en tiempo real.
- El bucle continúa ejecutándose, actualizando la información y tomando decisiones a intervalos de 1 segundo.

Este proceso automatizado permite a los usuarios rastrear el precio de Bitcoin y tomar decisiones rápidas basadas en datos actualizados en tiempo real.


```python
cont = 0

while(True):
  clear_output()
  print(f'REFRESH N°: {cont}\n')
  df_bitcoin = importar_base_bitcoin()
  precio, tendencia = extraer_tendencias("BTC")
  print(f'Precio actual: {precio}\n')
  print(f'Tendencia: {tendencia}\n')
  # limpieza_datos()
  media = 27000
  decision = tomar_desiciones(precio, media, tendencia)
  print(f'Decición: {decision}\n')
  visualizacion(df_bitcoin, precio, media, decision)
  cont = cont + 1
  time.sleep(1)
```
<img src="https://github.com/pabloing93/Trading-Robot/blob/dev/visualizacion_bitcoin.png" alt="Gráfico de ejemplo">

