import ssd1306                 # Display oled
import json                    # Manipular archivos Json
from machine import Pin, I2C   # Control pines y puerto I2C
import bluetooth
from ble_uart_peripheral import BLEUART

ble = bluetooth.BLE()
ble_uart = BLEUART(ble)

button = Pin(14, Pin.IN, Pin.PULL_DOWN)
led = Pin(15, Pin.OUT)

i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)

while True:
    if button.value():
        oled.fill(0)
        oled.text("Button pressed", 0, 0)
        oled.show()
        ble_uart.write("Button pressed\r\n")

    # queries if there is received data stored in the buffer
    if ble_uart.any():
        data = ble_uart.read()  # reads the data removing it from the buffer

        if data == b'on_off\r\n':
            led.value(not led.value())

            if led.value():
                oled.fill(0)
                oled.text("LED: On", 0, 0)
                oled.show()

            else:
                oled.fill(0)
                oled.text("LED: Off", 0, 0)
                oled.show()
        else:
            ble_uart.write('Command is not recognized\r\n"')

            oled.fill(0)
            oled.text("Command error", 0, 0)
            oled.show()