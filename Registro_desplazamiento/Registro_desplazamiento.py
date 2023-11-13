"""
Plantilla base para programar una Raspberry Pi Pico W para
controlar un registro de desplazamiento

"""

from machine import Pin

data = Pin(10, Pin.OUT)
latch = Pin(11, Pin.OUT)
clock = Pin(12, Pin.OUT)


def turnOnLed(status_led):
    latch.value(0)

    for led in status_led:
        clock.value(0)
        data.value(led)
        clock.value(1)

    latch.value(1)


# Lista de prueba
lista_led = [1, 0, 0, 1, 0, 0, 1, 0]

turnOnLed(lista_led)
