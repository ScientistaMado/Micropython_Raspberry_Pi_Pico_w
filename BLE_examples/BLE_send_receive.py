# Import necessary modules
from machine import Pin
import time
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral


ble = bluetooth.BLE()

sp = BLESimplePeripheral(ble)

led = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)
led_state = 0


def on_rx(data):
    print("Data received: ", data)
    if data == b'on_off\r\n':
        led.value(not led.value())
        if led.value():
            print('LED encendido')
        else:
            print('LED Apagado')


while True:
    if sp.is_connected():

        sp.on_write(on_rx)

        if button.value():
            sp.send("button pressed\n")
            print("Boton presionado")
            time.sleep(0.1)
