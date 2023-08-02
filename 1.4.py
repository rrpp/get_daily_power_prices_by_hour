import requests
from datetime import date
import datetime
import csv
import json
import os

def obtener_precio_luz():
    url = "https://api.preciodelaluz.org/v1/prices/all?zone=PCB"
    response = requests.get(url)
    data = response.json()
    print("precios obtenidos satisfactoriamiente", datetime.datetime.now())

    precios_luz = {}
    for clave, valor in data.items():
        # Obtener la fecha, hora y el valor del precio
        fecha = valor["date"]
        hora = valor["hour"]
        precio = round(valor["price"] / 1000, 4)

        # Almacenar la hora como clave y el precio como valor en el diccionario
        precios_luz[hora] = {"fecha": fecha, "precio_kwh": precio}

    # Devolver el diccionario con los precios de la luz por horas
    return precios_luz

print("ejecucion: ", datetime.datetime.now())
# Ejemplo de uso
precios_luz = obtener_precio_luz()
today = date.today()
fecha_actual = today.strftime("%Y-%m-%d")

# Rutas absolutas para el archivo CSV y el archivo JSON con el nombre del día actual
ruta_absoluta_csv = f"/home/alfonso/data/precios_luz_{fecha_actual}.csv"
ruta_absoluta_json = f"/home/alfonso/data/precios_luz_{fecha_actual}.json"


# Abrir el archivo CSV en modo escritura
with open(ruta_absoluta_csv, mode='w', newline='') as file:
    # Definir los nombres de las columnas
    fieldnames = ['Fecha', 'Hora', 'Precio (€/kWh)']

    # Crear el objeto writer para escribir en el archivo CSV
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Escribir la primera fila con los nombres de las columnas
    writer.writeheader()

    # Escribir los datos en el archivo CSV
    for hora, data in precios_luz.items():
        writer.writerow({'Fecha': data['fecha'], 'Hora': hora, 'Precio (€/kWh)': data['precio_kwh']})

print(f"Los datos se han almacenado en el archivo {ruta_absoluta_csv}", datetime.datetime.now())


# Escribir los datos en el archivo JSON
with open(ruta_absoluta_json, mode='w') as file:
    json.dump(precios_luz, file)

print(f"Los datos se han almacenado en el archivo {ruta_absoluta_json}:", datetime.datetime.now())
