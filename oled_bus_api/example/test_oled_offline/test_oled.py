
import network                 # Para gestionar la conexión a la red
import gc                      # Para recolección de basura
import time                    # Para manejar el tiempo
import ssd1306                 # Display oled
import json                    # Manipular archivos Json
from machine import Pin, I2C   # Control pines y puerto I2C


# Gestion automáticamente la memoria
gc.collect()

SSID = 'YOUR SSID'        # Nombre de la red WiFi
PASSWORD = 'YOUR PASS'    # Contraseña de la red WiFi


def connectWifi(ssid, password):
    # Inicializar la interfaz de estación

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    oled.text("Conectando", 10, 10)
    oled.show()
    dot = 10

    while not station.isconnected():
        print('conectando')
        oled.text(".", dot, 20)
        oled.show()
        time.sleep(1)
        dot += 6

    print(f'Conectado con éxito a {ssid}')

    oled.fill(0)
    oled.text("Conectado", 10, 10)
    oled.show()


def showInOled(stop_bus_info, bus_id):
    ''''
    Muestra en el display oled la información del bus
    más cercano a partir de la información del paradero
    y el id del recorrido del bus
    '''

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

# Abre el documento y carga los datos json
with open("example_response.json", "r") as file:
    data = json.loads(file)

# Modifica '229' por el recorrido que deseas consultar
showInOled(data, '229')
