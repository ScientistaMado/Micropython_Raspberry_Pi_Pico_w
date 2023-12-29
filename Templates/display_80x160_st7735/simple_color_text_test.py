from st7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin
import time
import math

# sck 18
# sda 19
# miso 16 No es necesario
spi = SPI(0, baudrate=20000000)

# TFT(spi, DC, Reset, CS)
tft = TFT(spi, 21, 20, 17)

tft.initr()
tft.rgb()
tft.invertcolor(True)


def test_main():
    tft.fill(TFT.BLACK)
    tft.text((0, 10), "Hola", TFT.GREEN, sysfont, 2)
    tft.text((0, 40), "Hola Caracola", TFT.GREEN, sysfont, 2)
    time.sleep_ms(1000)
    tft.fill(TFT.GREEN)
    time.sleep_ms(1000)
    tft.fill(TFT.RED)
    time.sleep_ms(1000)


tft.rotation(1)
tft.setStart(0, 26)
while True:
    test_main()
