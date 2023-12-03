from machine import Pin, I2C
from menuoled import MENU, MENU_ICONS, NAVIGATE_MENU
from bme280 import BME280
from encoder import Rotary
from sh1106 import SH1106_I2C
from time import sleep

var = 0


def show_main_menu():
    oled_option.centerText(BME280)
    main_menu.draw()


def show_temp():
    global var
    var = "temp"
    show_main_menu()


def show_hum():
    global var
    var = "hum"


def show_press():
    global var
    var = "press"


def show_all():
    global var
    var = "all"


i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SH1106_I2C(128, 64, i2c, rotate=180)
bme = BME280(i2c=i2c)

main_menu = MENU_ICONS(oled, n_icons_x=4, n_icons_y=1)

main_menu.add_option("temperatura", show_temp, 1, 0)
main_menu.add_option("humedad", show_hum, 0, 0)
main_menu.add_option("presion", show_press, 2, 0)
main_menu.add_option("todo", show_all, 3, 0)

oled_option = MENU(oled)

menu_list = [main_menu]

menu = NAVIGATE_MENU(menu_list)
