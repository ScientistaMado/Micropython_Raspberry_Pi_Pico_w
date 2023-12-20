import network  # Para gestionar la conexión a la red
import gc       # Para recolección de basura
import time     # Para manejar el tiempo
import urequests as requests   # Para realizar solicitudes HTTP
import framebuf                # Para trabajar con imágenes
import json                    # Manipular archivos Json
from sh1106 import SH1106_I2C  # Controla el display oled
from machine import Pin, I2C   # Configuración de pines y comunicación i2c
from time import sleep         # Manejar tiempos


# Limpiar la memoria
gc.collect()

SSID = 'YOUR SSID'            # Nombre de la red WiFi
PASSWORD = 'YOUR PASSWORD'    # Contraseña de la red WiFi

# URL de la API que estás utilizando
URL_BASE = "https://api.coingecko.com/api/v3"

# Tu clave API
API_KEY = "YOUR_API_KEY"


def connectWifi(ssid, password, timeout=15):

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    oled.fill(0)
    oled.show()

    oled.text("Conectando", 10, 0)
    oled.show()
    dot = 10
    timeout_connect = 0

    while not station.isconnected():
        print('conectando')

        oled.text(".", dot, 20)
        oled.show()
        time.sleep(1)
        timeout_connect += 1
        dot += 6

        if timeout_connect >= timeout:

            oled.fill(0)
            oled.text("No se pudo", 10, 20)
            oled.text(f"conectara {ssid}", 10, 30)

            raise Exception(f"No se pudo conectar a {ssid}")

    print(f'Conexión exitosa a {ssid}')

    oled.fill(0)
    oled.text("Conectado", 10, 0)
    oled.show()


def fetch_api_simple_price(url_base: str, api_key: str, coin_info_list: dict, timeout=15):

    # Encabezados de la solicitud con la clave API
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + api_key
               }

    # URL base para este tipo de splicitud
    url = url_base + "/simple/price?ids="

    # Agregaa las monedas a consultar
    for index in range(len(coin_info_list['coins'])):
        url += f'%2C{coin_info_list["coins"][index].lower()}'

    # Incluye la comparación (Por el momento solo admite una comparación)
    url += f'&vs_currencies={coin_info_list["coin_vs"].lower()}'

    parameters = coin_info_list.items()

    for key, value in parameters:
        if isinstance(value, bool):
            if value:
                url += f'&{key}={str(value).lower()}'

    try:
        response = requests.get(url, headers=headers, timeout=timeout)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print('Error en la solicitud. Código de respuesta HTTP:',
                  response.status_code)
            return None

    except Exception as e:
        print('Error en la solicitud:', str(e))
        return None


def infoIcon(icon_id):

    with open(f'icons/{icon_id}.pbm', "rb") as file:
        file.readline()
        xy = file.readline()
        x = int(xy.split()[0])
        y = int(xy.split()[1])
        icon = bytearray(file.read())

        icon_array = framebuf.FrameBuffer(icon, x, y, framebuf.MONO_HLSB)

    return [x, y, icon_array]


def showInOled(data_coins, coin_search, vs_coin):

    info_coin = data_coins[coin_search]
    valor = info_coin[vs_coin]

    if valor < 100:
        valor = f'{valor:0.2f}'

    change_24h = info_coin[f'{vs_coin}_24h_change']
    change_24h = f'{change_24h:0.2f}'

    # change_24h = str(change_24h)

    icon_data = infoIcon(coin_search)

    def center_coin_name(name_coin, x_icon, x_icon_pos):
        x = (oled.width + x_icon + x_icon_pos - len(name_coin)*8)//2
        y = (icon_data[1]//2)-4

        name = name_coin.upper()
        oled.text(name, x, y)
        oled.hline(x, y+9, len(name_coin)*8, 1)

    def centerText(text, y):
        x = (oled.width - len(text)*8)//2
        oled.text(text, x, y)

    oled.fill(0)

    oled.blit(icon_data[2], 20, 0)
    center_coin_name(coin_search, icon_data[0], 10)

    centerText(f'{valor} {vs_coin}', icon_data[1]+8)
    centerText(f'{change_24h} %', icon_data[1]+20)

    oled.show()


coin_info = {"coins": ["bitcoin", "ethereum", "solana", "cardano"],
             "coin_vs": "usd",
             "include_market_cap": False,
             "include_24hr_change": True,
             "include_24hr_vol": False,
             }


i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SH1106_I2C(128, 64, i2c, rotate=180)

# Conectar a la red WiFi
connectWifi(SSID, PASSWORD)

data = fetch_api_simple_price(URL_BASE, API_KEY, coin_info)

# Imprimir la respuesta
print(data)

while True:
    showInOled(data, "cardano", coin_info["coin_vs"])
    sleep(20)
    showInOled(data, "bitcoin", coin_info["coin_vs"])
    sleep(20)
    showInOled(data, "ethereum", coin_info["coin_vs"])
    sleep(20)
    showInOled(data, "solana", coin_info["coin_vs"])
    sleep(20)
