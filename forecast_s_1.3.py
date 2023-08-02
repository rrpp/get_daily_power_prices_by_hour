import requests
from datetime import datetime, timedelta
import json
import csv
import os

def obtener_temperatura_pronostico(api_key):
    # Función para obtener el pronóstico de temperatura
    latitud = 40.0271087
    longitud = -3.9115161
    url_pronostico = f'https://api.openweathermap.org/data/2.5/onecall?lat={latitud}&lon={longitud}&exclude=current,minutely,daily&appid={api_key}&units=metric'

    try:
        # Realizar una solicitud a la API de OpenWeather para obtener el pronóstico
        response_pronostico = requests.get(url_pronostico)
        response_pronostico.raise_for_status()  # Comprobar si la solicitud fue exitosa (sin errores HTTP)

        # Convertir los datos de respuesta a formato JSON
        datos_pronostico = response_pronostico.json()

        pronostico = {}

        # Obtener el pronóstico desde las 00:00 hasta las 23:00 horas del mismo día
        base_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)  # Obtener la hora actual y ponerla a las 00:00:00
        for hora in range(24): # solo crea un range de 24, como un for de 24 iteraciones
            print(hora)
            fecha_hora = base_time + timedelta(hours=hora)  # Generar la fecha e incrementar las horas para cada pronóstico horario
            print(fecha_hora)
            temperatura = datos_pronostico['hourly'][hora]['temp']  # Obtener la temperatura del pronóstico horario
            print(temperatura)
            pronostico[fecha_hora] = temperatura  # Guardar la temperatura en el diccionario de pronóstico

        return pronostico

    except requests.exceptions.RequestException as e:
        print(f'Error al obtener el pronóstico: {e}')
        return {}


# Clave de API de OpenWeatherMap
api_key = '2d8ca1ebd16e649b7c241d3b14500b13'

# Generar el pronóstico de temperatura
forecast = obtener_temperatura_pronostico(api_key)

# Mostrar el pronóstico para cada hora desde las 00:00:00 hasta las 23:00:00
for hora, temperatura in forecast.items():
    print(f"{hora.strftime('%H:%M:%S')}: {temperatura}°C")

#===============================


# Obtener la fecha actual para formar el nombre de los archivos
fecha_actual = datetime.now().strftime('%Y-%m-%d')

# Crear la carpeta específica en Ubuntu (si no existe)
carpeta_destino = f'/home/alfonso/data/{fecha_actual}/'  # Reemplaza con la ruta real de la carpeta
import os
os.makedirs(carpeta_destino, exist_ok=True)

# Convertir las claves del diccionario de datetime a cadenas
forecast_str_keys = {hora.strftime('%Y-%m-%d %H:%M:%S'): temperatura for hora, temperatura in forecast.items()}

# Guardar el pronóstico en formato JSON
json_file = os.path.join(carpeta_destino, f'pronostico_temperatura_{fecha_actual}.json')
with open(json_file, 'w') as f:
    json.dump(forecast_str_keys, f, indent=4)

# Guardar el pronóstico en formato CSV
csv_file = os.path.join(carpeta_destino, f'pronostico_temperatura_{fecha_actual}.csv')
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Fecha y Hora', 'Temperatura (°C)'])
    for hora, temperatura in forecast.items():
        writer.writerow([hora.strftime('%Y-%m-%d %H:%M:%S'), temperatura])

# Mostrar el pronóstico para cada hora desde las 00:00:00 hasta las 23:00:00
for hora, temperatura in forecast.items():
    print(f"{hora.strftime('%H:%M:%S')}: {temperatura}°C")