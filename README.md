# Trading Robot 🤖

## Tecnologías utilizadas 📊

### Pandas
Pandas es una biblioteca esencial para el análisis y manipulación de datos en Python. Muy utilizada en proyectos de Ciencia de Datos.

### BeautifulSoup (bs4)
BeautifulSoup es una biblioteca utilizada para técnicas de webscraping. La utilizamos en nuestro proyecto para obtener datos de Coinmarket.

### Matplotlib Pyplot
Una biblioteca de visualización de datos en Python. Nos facilita la creación de gráficos y mejor comprensión de la distribución de los datos a través de visualizaciones.

### Yfinance
Yfinance es una herramienta open source que nos proporciona una API para acceder a datos financieros y del mercado en tiempo real.


## Etapas del algoritmo

## Configuración del ambiente
> [!IMPORTANT] 
> Se requiere instalar las tecnologías necesarias para poder ejecutar el proyecto de manera local
> ```
> pip install pandas, matplotlib, yfinance, beautifulsoup4
> ```

## Obtencion de datos 📁

La función importar_base_bitcoin() utiliza la API de yfinance para obtener datos históricos de Bitcoin durante los últimos 7 días con intervalos de 5 minutos.
Llamamos a la función y almacenamos su valor en una variable como se muestra a continuación:

![image](https://github.com/pabloing93/Trading-Robot/assets/32267303/039b9c9a-0315-4199-8a49-dc860e84e24c)



[<kbd> <br> code link <br> </kbd>][KBD]

[KBD]: f221f39a64f4846224f8496a8a094dc92aecfdac/functions.py#L9

La función extraer_tendencias() recibe como parámetro "BTC" que es el símbolo de la moneda de la cuál extraeremos la información del precio y la tendencia.
Llamamos a la función y almacenamos su valor en una variable como se muestra a continuación:

![image](https://github.com/pabloing93/Trading-Robot/assets/32267303/472c4f45-f544-4dc7-bcf2-ba72411739c3)
![image](https://github.com/pabloing93/Trading-Robot/assets/32267303/820ac7d5-4b1e-4e93-97b3-1bad6a5441f2)

[<kbd> <br> code link <br> </kbd>][KBD]

[KBD]: f221f39a64f4846224f8496a8a094dc92aecfdac/functions.py#L15

Procedimiento:
Utilizando el símbolo de la moneda aplicamos webscraping a la página web https://coinmarketcap.com/ 
Obtenemos el precio y la tendencia en 1h %
<img src="https://github.com/pabloing93/Trading-Robot/blob/master/images/2_coinmarket.png" alt="visualizacion">


## Depuración de los datos 🧹

La depuración de los datos se realiza a través de la función limpieza_datos()

![image](https://github.com/pabloing93/Trading-Robot/assets/32267303/16156cd0-f087-4dfd-80b9-5f80e8a1c54e)

Que se encuentra definida de la siguiente forma
![image](https://github.com/pabloing93/Trading-Robot/assets/32267303/8ab38bb2-aec3-4ad0-bffc-31bd84fd3af0)

[<kbd> <br> code link <br> </kbd>][KBD]

[KBD]: f221f39a64f4846224f8496a8a094dc92aecfdac/functions.py#L64

1. Hacemos una copia de ```df_bitcoin```
2. Eliminamos los registros duplicados de la columna ```Datetime```.
3. Eliminamos los registros cuyo valor en la columna ```Close``` sea nulo o 0.
4. Nos quedamos con los registros cuyo valor en columna ```Volume``` sea mayor a 0.
5. Identifica y eliminanos los "outliers" del precio de cierre de Bitcoin.

<img src="https://github.com/pabloing93/Trading-Robot/blob/master/images/boxplot1.png" alt="Gráfico Data Original">

6. Agrupamos los datos que se encuentren entre el primer y el tercer Quartil ```Q3 > Close > Q1```
7. Obtenemos el valor de la media desde los datos depurados

<img src="https://github.com/pabloing93/Trading-Robot/blob/master/images/boxplot2.png" alt="Gráfico Data Limpio">

En resumen, este código se encarga de asegurarse de que los datos relacionados con el precio de Bitcoin sean precisos y útiles para futuros análisis. Esto implica eliminar datos duplicados, nulos e inusuales, y calcular el precio promedio después de realizar estas limpiezas.

## Toma de decisiones 🚀

![image](https://github.com/pabloing93/Trading-Robot/assets/32267303/abc8427a-5b2e-4e30-8e6d-8b92b909a36d)

![image](https://github.com/pabloing93/Trading-Robot/assets/32267303/6c754c05-3639-4ef7-b909-77b762413d09)

[<kbd> <br> code link <br> </kbd>][KBD]

[KBD]: f221f39a64f4846224f8496a8a094dc92aecfdac/functions.py#L87

El algoritmo de toma de decisiones consiste en analizar el precio actual de la moneda, el precio promedio y la tendencia.
  - Caso 1: Si el precio actual es mayor o igual al precio promedio y la tendencia es "baja", entonces se recomienda "Vender".
  - Caso 2: Si el precio actual es menor que el precio promedio y la tendencia es "alta", entonces recomienda "Comprar".
- Si ninguno de estos casos se cumple, se recomienda "Esperar".

Finalmente, la función devuelve una decisión, que puede ser "Vender", "Comprar" o "Esperar" en función de los valores de entrada.

## Visualizacion 📈
En éste procedimiento del algoritmo mostramos los resultados en un gráfico para facilitar su comprensión de los datos resultados y dar apoyo en la toma de decisiones.

![image](https://github.com/pabloing93/Trading-Robot/assets/32267303/29d31358-0d9f-4408-86c1-055dc03dc021)
![image](https://github.com/pabloing93/Trading-Robot/assets/32267303/311369ce-af57-4af3-ba1b-fc783e3eba18)
[<kbd> <br> code link <br> </kbd>][KBD]

[KBD]: f221f39a64f4846224f8496a8a094dc92aecfdac/functions.py#L99

<img src="https://github.com/pabloing93/Trading-Robot/blob/master/images/prices.png" alt="visualizacion">

## Automatizacion 🧠

Este proceso automatizado permite a los usuarios rastrear el precio de Bitcoin y tomar decisiones rápidas basadas en datos actualizados en tiempo real.

![image](https://github.com/pabloing93/Trading-Robot/assets/32267303/79c7c2d9-5b5d-47e6-a15f-a6db2f414068)

