""" 
Este código es la base para conectar una Raspberry Pi Pico W a una red WiFi y realizar una solicitud a una API.

1. Se importan las bibliotecas necesarias y se realiza una recolección de basura para liberar memoria.
2. Se configuran las credenciales de la red WiFi y la URL de la API a la que se va a acceder.
3. Se define una función para conectarse a la red WiFi y otra para obtener datos de la API.
4. Después de conectarse con éxito a la red WiFi, se realiza una solicitud a la API y se muestra la respuesta.

"""


import network  # Para gestionar la conexión a la red
import gc       # Para recolección de basura
import time     # Para manejar el tiempo
import urequests as requests  # Para realizar solicitudes HTTP

# Limpiar la memoria
gc.collect()

SSID = 'TU SSID'        # Nombre de la red WiFi
PASSWORD = 'TU PASS'    # Contraseña de la red WiFi
URL_API = 'TU URL API'  # URL de la API a la que se va a acceder

# Función para conectar a la red WiFi


def connectWifi(ssid, password):
    # Inicializar la interfaz de estación

    station = network.WLAN(network.STA_IF)
    station.active(True)                    # Activar la interfaz
    station.connect(ssid, password)

    while not station.isconnected():
        print('Conectando...')
        time.sleep(1)

    print(f'Conexión exitosa a {ssid}')


def fetchApi(api_url, timeout=10):
    # Función para obtener datos de la API

    try:
        # Realizar una solicitud GET
        response = requests.get(api_url, timeout=timeout)

        if response.status_code == 200:
            return response.text
        else:
            print('Error en la solicitud. Código de respuesta HTTP:',
                  response.status_code)
            return None

    except Exception as e:
        print('Error en la solicitud:', str(e))
        return None


# Conectar a la red WiFi
connectWifi(SSID, PASSWORD)

# Se solicitan los datos e imprimen en consola
data = fetchApi(URL_API)
print(data)
