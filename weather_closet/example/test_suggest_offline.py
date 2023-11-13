import esp
import gc
import time
import sh1106
import framebuf
from clothingmanager import ClothingManager
from machine import Pin, I2C


esp.osdebug(None)
gc.collect()


data_dicts = [
    {"Temperatura Mínima": "12",
     "Temperatura Máxima": "20",
     "Día": "Lunes",
     "Símbolo del tiempo": "1"},

    {"Temperatura Mínima": "12",
     "Temperatura Máxima": "16",
     "Día": "Martes",
     "Símbolo del tiempo": "4"},

    {"Temperatura Mínima": "2",
     "Temperatura Máxima": "12",
     "Día": "Miércoles",
     "Símbolo del tiempo": "7"},

    {"Temperatura Mínima": "3",
     "Temperatura Máxima": "14",
     "Día": "Jueves",
     "Símbolo del tiempo": "9"},

    {"Temperatura Mínima": "8",
     "Temperatura Máxima": "15",
     "Día": "Viernes",
     "Símbolo del tiempo": "12"},

    {"Temperatura Mínima": "16",
     "Temperatura Máxima": "23",
     "Día": "Sábado",
     "Símbolo del tiempo": "2"},

    {"Temperatura Mínima": "15",
     "Temperatura Máxima": "19",
     "Día": "Domingo",
     "Símbolo del tiempo": "4"},
]


def openIcon(icon_id):

    with open(f'icons/{icon_id}.pbm', "rb") as file:
        file.readline()
        xy = file.readline()
        x = int(xy.split()[0])
        y = int(xy.split()[1])
        icon = bytearray(file.read())

    return framebuf.FrameBuffer(icon, x, y, framebuf.MONO_HLSB)


def showInOled(data):
    oled.fill(0)

    day = data["Día"]
    day_x = int((128 - (len(day)*8))/2)

    if day == "Miércoles":
        day = "Miercoles"
    if day == "Sábado":
        day = "Sabado"

    oled.text(day, day_x, 2)

    t = f'{data["Temperatura Mínima"]}-{data["Temperatura Máxima"]}C'
    t_x = int((128 - (len(t)*8))/2)

    oled.text(t, t_x, 18)

    icon_id = data["Símbolo del tiempo"]
    oled.blit(openIcon(icon_id), 48, 32)

    oled.show()


i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
oled = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
oled.sleep(False)
oled.fill(0)

data_pin = Pin(13, Pin.OUT)
clk_pin = Pin(14, Pin.OUT)
latch_pin = Pin(12, Pin.OUT)

clothing_manager = ClothingManager(data_pin, clk_pin, latch_pin)

for data_dict in data_dicts:

    showInOled(data_dict)
    print(data_dict)
    clothing_manager.suggestOutfit(data_dict)
    time.sleep(2)
