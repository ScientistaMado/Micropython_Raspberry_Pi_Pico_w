# Import necessary modules
from machine import Pin
import time
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral


# Create object BLE
ble = bluetooth.BLE()

# Create object Simple peripheral and active BLE
sp = BLESimplePeripheral(ble)

# Configure the LED pin as output and the button pin as pulldown
led = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)


def on_rx(data):
    """"
    function that is executed when the on_off data is received\r\n
    """
    print("Data received: ", data)
    if data == b'on_off\r\n':
        led.value(not led.value())
        if led.value():
            print('LED encendido')
        else:
            print('LED Apagado')


while True:

    if sp.is_connected():
     # If there is data received

        sp.on_write(on_rx)  # Execute the on_rx function

    if button.value():
        # If button is pressed, sends button pressed

        sp.send("button pressed\n")
        print("Boton presionado")
        time.sleep(0.1)
