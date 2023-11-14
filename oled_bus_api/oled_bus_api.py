import network                 # Para gestionar la conexión a la red
import gc                      # Para recolección de basura
import time                    # Para manejar el tiempo
import urequests as requests   # Para realizar solicitudes HTTP
import ssd1306                 # Display oled
import framebuf                # Para trabajar con imágenes
import json                    # Manipular archivos Json
from machine import Pin, I2C

# Gestion automáticamente la memoria
gc.collect()

SSID = 'YOUR SSID'        # Nombre de la red WiFi
PASSWORD = 'YOUR PASS'    # Contraseña de la red WiFi


# URL de la API a la que se va a acceder
URL_API = 'https://api.xor.cl/red/bus-stop/'


def connectWifi(ssid, password):
    # Inicializar la interfaz de estación

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    oled.fill(0)
    oled.show()
    oled.text("Conectando", 10, 0)
    oled.show()
    dot = 10

    while not station.isconnected():
        print('conectando')
        oled.text(".", dot, 20)
        oled.show()
        time.sleep(1)
        dot += 6

    print(f'Conexión exitosa a {ssid}')

    oled.fill(0)
    oled.text("Conectado", 10, 0)
    oled.show()


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


def openIcon(icon_id):

    with open(f'icons/{icon_id}.pbm', "rb") as file:
        file.readline()
        xy = file.readline()
        x = int(xy.split()[0])
        y = int(xy.split()[1])
        icon = bytearray(file.read())

    return framebuf.FrameBuffer(icon, x, y, framebuf.MONO_HLSB)


def showInOled(stop_bus_info, bus_id):
    """
    Muestra en el display oled la información del bus
    más cercano a partir de la información del paradero
    y el id del recorrido del bus
    """

    id_stop_bus = stop_bus_info['id']
    services = stop_bus_info['services']

    for service in services:
        if service['id'] == bus_id and service['valid']:
            bus = service['id']
            distance = service['buses'][0]['meters_distance']
            min_time = service['buses'][0]['min_arrival_time']
            max_time = service['buses'][0]['max_arrival_time']

    def oledCenterText(text, y):
        x = int((128 - len(text)*8)/2)
        oled.text(text, x, y)

    time_interval = f'{min_time} - {max_time} min'
    d = f'{distance} m'

    oled.fill(0)
    oled.blit('icon_bus', 0, 10)
    oled.text(id_stop_bus, 27, 0)
    oled.text(bus_id, 27, 8)
    oledCenterText(d, 16)
    oledCenterText(time_interval, 24)
    oled.show()


i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)


# Conectar a la red WiFi
connectWifi(SSID, PASSWORD)


# Modifica 'PG335' por el paradero que deseas consultar
data = fetchApiBus(URL_API, 'PG335')

# Modifica '229' por el recorrido que deseas consultar
showInOled(data, '229')
