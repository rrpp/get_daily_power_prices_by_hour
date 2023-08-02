import requests
from datetime import date
import datetime
import csv
import json
import os

def obtener_precio_luz():
    url = "https://api.preciodelaluz.org/v1/prices/all?zone=PCB"
    # Resto del código para obtener los datos... (omitiendo por simplicidad)
    precio_descargado= {"00-01":{"date":"02-08-2023","hour":"00-01","is-cheap":True,"is-under-avg":True,"market":"PVPC","price":124.72,"units":"\u20ac/MWh"},"01-02":{"date":"02-08-2023","hour":"01-02","is-cheap":False,"is-under-avg":True,"market":"PVPC","price":126.77,"units":"\u20ac/MWh"},"02-03":{"date":"02-08-2023","hour":"02-03","is-cheap":False,"is-under-avg":True,"market":"PVPC","price":126.89,"units":"\u20ac/MWh"},"03-04":{"date":"02-08-2023","hour":"03-04","is-cheap":False,"is-under-avg":True,"market":"PVPC","price":126.81,"units":"\u20ac/MWh"},"04-05":{"date":"02-08-2023","hour":"04-05","is-cheap":False,"is-under-avg":True,"market":"PVPC","price":124.95,"units":"\u20ac/MWh"},"05-06":{"date":"02-08-2023","hour":"05-06","is-cheap":False,"is-under-avg":True,"market":"PVPC","price":124.85,"units":"\u20ac/MWh"},"06-07":{"date":"02-08-2023","hour":"06-07","is-cheap":True,"is-under-avg":True,"market":"PVPC","price":124.26,"units":"\u20ac/MWh"},"07-08":{"date":"02-08-2023","hour":"07-08","is-cheap":False,"is-under-avg":True,"market":"PVPC","price":127.17,"units":"\u20ac/MWh"},"08-09":{"date":"02-08-2023","hour":"08-09","is-cheap":False,"is-under-avg":False,"market":"PVPC","price":148.92,"units":"\u20ac/MWh"},"09-10":{"date":"02-08-2023","hour":"09-10","is-cheap":False,"is-under-avg":True,"market":"PVPC","price":130.04,"units":"\u20ac/MWh"},"10-11":{"date":"02-08-2023","hour":"10-11","is-cheap":False,"is-under-avg":False,"market":"PVPC","price":167.03,"units":"\u20ac/MWh"},"11-12":{"date":"02-08-2023","hour":"11-12","is-cheap":False,"is-under-avg":False,"market":"PVPC","price":163.68,"units":"\u20ac/MWh"},"12-13":{"date":"02-08-2023","hour":"12-13","is-cheap":False,"is-under-avg":False,"market":"PVPC","price":163.33,"units":"\u20ac/MWh"},"13-14":{"date":"02-08-2023","hour":"13-14","is-cheap":False,"is-under-avg":False,"market":"PVPC","price":162.2,"units":"\u20ac/MWh"},"14-15":{"date":"02-08-2023","hour":"14-15","is-cheap":True,"is-under-avg":True,"market":"PVPC","price":99.93,"units":"\u20ac/MWh"},"15-16":{"date":"02-08-2023","hour":"15-16","is-cheap":True,"is-under-avg":True,"market":"PVPC","price":72.95,"units":"\u20ac/MWh"},"16-17":{"date":"02-08-2023","hour":"16-17","is-cheap":True,"is-under-avg":True,"market":"PVPC","price":77.23,"units":"\u20ac/MWh"},"17-18":{"date":"02-08-2023","hour":"17-18","is-cheap":True,"is-under-avg":True,"market":"PVPC","price":104.84,"units":"\u20ac/MWh"},"18-19":{"date":"02-08-2023","hour":"18-19","is-cheap":False,"is-under-avg":False,"market":"PVPC","price":165.2,"units":"\u20ac/MWh"},"19-20":{"date":"02-08-2023","hour":"19-20","is-cheap":False,"is-under-avg":False,"market":"PVPC","price":169.95,"units":"\u20ac/MWh"},"20-21":{"date":"02-08-2023","hour":"20-21","is-cheap":False,"is-under-avg":False,"market":"PVPC","price":192.86,"units":"\u20ac/MWh"},"21-22":{"date":"02-08-2023","hour":"21-22","is-cheap":False,"is-under-avg":False,"market":"PVPC","price":197.71,"units":"\u20ac/MWh"},"22-23":{"date":"02-08-2023","hour":"22-23","is-cheap":False,"is-under-avg":False,"market":"PVPC","price":152.67,"units":"\u20ac/MWh"},"23-24":{"date":"02-08-2023","hour":"23-24","is-cheap":False,"is-under-avg":False,"market":"PVPC","price":151.99,"units":"\u20ac/MWh"}}

    precios_luz = {}
    for clave, valor in precio_descargado.items():
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
