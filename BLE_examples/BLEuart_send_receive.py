from machine import Pin
import bluetooth
from ble_uart_peripheral import BLEUART

ble = bluetooth.BLE()
ble_uart = BLEUART(ble)

button = Pin(14, Pin.IN, Pin.PULL_DOWN)
led = Pin(15, Pin.OUT)

while True:
    if button.value():
        ble_uart.write("Button pressed\r\n")

    # queries if there is received data stored in the buffer
    if ble_uart.any():
        data = ble_uart.read()  # reads the data removing it from the buffer

        if data == b'on_off\r\n':
            led.value(not led.value())
        else:
            ble_uart.write('Command is not recognized\r\n"')
