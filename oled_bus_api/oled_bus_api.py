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


def fetchApi(api_url, stop_bus_id, timeout=10):

    try:
        response = requests.get(api_url + stop_bus_id, timeout=timeout)

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

    id_stop_bus = stop_bus_info['id']
    services = stop_bus_info['services']

    for service in services:
        if service['id'] == bus_id:
            if service['valid']:
                distance = service['buses'][0]['meters_distance']
                min_time = service['buses'][0]['min_arrival_time']
                max_time = service['buses'][0]['max_arrival_time']

            else:
                print(service["status_description"])
                oled.fill(0)
                oled.text("Sin recorrido", 0, 30)
                oled.show()

    def oledCenterText(text, y):
        x = int((128 - len(text)*8)/2)
        oled.text(text, x, y)

    t = f'{min_time}-{max_time} min'
    d = f'{distance} m'

    oled.fill(0)

    oled.blit(openIcon('icon_bus'), 25, 0)
    oled.text(id_stop_bus, 50, 0)
    oled.text(bus_id, 50, 8)

    oledCenterText(d, 25)
    oledCenterText(t, 40)

    oled.show()


i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)

connectWifi(SSID, PASSWORD)

data = fetchApi(URL_API, 'PG335')

showInOled(data, '229')

print(data)
