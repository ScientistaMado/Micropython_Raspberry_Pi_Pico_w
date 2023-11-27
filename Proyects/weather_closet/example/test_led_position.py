from machine import Pin, I2C
import sh1106
import time

data_pin = Pin(13, Pin.OUT)
clk_pin = Pin(14, Pin.OUT)
latch_pin = Pin(12, Pin.OUT)


leds = [(0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),]


i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
oled = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
oled.sleep(False)
oled.fill(0)


def led_off():
    latch_pin.value(0)
    for led in [0]*16:
        clk_pin.value(0)
        data_pin.value(led)
        clk_pin.value(1)

    latch_pin.value(1)


led_off()

pos_led = 2

for led in leds:

    oled.fill(0)
    oled.text(f"pos_LED: {pos_led}", 10, 10)
    oled.show()
    pos_led += 1

    latch_pin.value(0)
    print(led)

    for status_led in led:
        clk_pin.value(0)
        data_pin.value(status_led)
        clk_pin.value(1)

    latch_pin.value(1)

    time.sleep(2)

led_off()
