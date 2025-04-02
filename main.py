from flask import Flask, render_template, redirect
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg') #warning main treath

# Buscar en ThingSpeak estaciones meteorológicas:
# https://thingspeak.mathworks.com/channels/public
# Ejemplos:
# https://thingspeak.mathworks.com/channels/870845
# https://thingspeak.mathworks.com/channels/1293177
# https://thingspeak.mathworks.com/channels/12397

URLs = [
  'https://api.thingspeak.mathworks.com/channels/870845/feeds.csv?results=8000',
  'https://api.thingspeak.mathworks.com/channels/1293177/feeds.csv?results=8000',
  'https://api.thingspeak.mathworks.com/channels/12397/feeds.csv?results=8000',
]

app = Flask(__name__)


def descargar(url):
  # descarga el URL en un dataframe, desde el URL
  df = pd.read_csv(url)
  #convertir la cadena en una fecha real
  df['created_at'] = pd.to_datetime(df['created_at'])
  #Borrar las columnas que no necesitamos
  if 'field6' in df.columns:
    df.drop(['entry_id', 'field5', 'field6'], axis=1, inplace=True)
  else:
    df.drop(['entry_id', 'field5', 'field7'], axis=1, inplace=True)

  # renombrar columnas
  df.columns = ['fecha', 'temp_exterior', 'temp_inferior', 'temp_atm', 'humedad']
  return df


def graficar(df):
    for columna in df.columns[1:]:
      #crear la figura
      fig = plt.figure(figsize=(8, 5))
      #hacemos la grafica
      plt.plot(df['fecha'], df[columna], label=columna)
      # poner los titulos
      plt.title(f"Historico de {columna}")
      # grabar la imagen
      plt.savefig(f"static/{columna}.png")
      plt.close()
    return lista
 
@app.route('/')
def index():
  # descargar los datos y crear las graficas
  for url in URLs:
    nombres = []
    df = descargar(url)
    nombres.extend(graficar(df))
  return render_template('index.html', nombres=nombres)

# Programa Principal
if __name__ == '__main__':
 app.run(host='0.0.0.0', debug=True)
