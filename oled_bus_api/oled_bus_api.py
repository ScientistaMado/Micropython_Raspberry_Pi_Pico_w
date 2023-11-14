import network  # Para gestionar la conexión a la red
import gc       # Para recolección de basura
import time     # Para manejar el tiempo
import urequests as requests  # Para realizar solicitudes HTTP
import ssd1306
import json
from machine import Pin, I2C

# Limpiar la memoria
gc.collect()

SSID = 'YOUR SSID'        # Nombre de la red WiFi
PASSWORD = 'YOUR PASS'    # Contraseña de la red WiFi
# URL de la API a la que se va a acceder
URL_API = 'https://api.xor.cl/red/bus-stop/'

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


def fetchApiBus(api_url, stop_bus, timeout=10):
    # Función para obtener datos de la API

    try:
        # Realizar una solicitud GET
        response = requests.get(api_url+stop_bus, timeout=timeout)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print('Error en la solicitud. Código de respuesta HTTP:',
                  response.status_code)
            return None

    except Exception as e:
        print('Error en la solicitud:', str(e))
        return None


def showInOled(stop_bus_info, bus_id):
    id_stop_bus = stop_bus_info['id']
    services = stop_bus_info['services']

    for service in services:
        if service['id'] == bus_id and service['valid']:
            bus = service['id']
            distance = service['buses'][0]['meters_distance']
            min_time = service['buses'][0]['min_arrival_time']
            max_time = service['buses'][0]['max_arrival_time']

    oled.fill(0)
    oled.text(id_stop_bus, 0, 0)
    oled.text(str(bus), 0, 8)
    oled.text(str(distance), 0, 16)
    oled.text(str(min_time), 0, 24)
    oled.text(str(max_time), 0, 32)
    oled.show()


i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)


# Conectar a la red WiFi
connectWifi(SSID, PASSWORD)

# Se solicitan los datos e imprimen en consola
data = fetchApiBus(URL_API, 'PG335')
showInOled(data, '229')

print(data)
