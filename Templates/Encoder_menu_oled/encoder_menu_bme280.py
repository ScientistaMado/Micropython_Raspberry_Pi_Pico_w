from machine import Pin, I2C
from menuoled import MENU, MENU_ICONS, NAVIGATE_MENU
from bme280 import BME280
from encoder import Rotary
from sh1106 import SH1106_I2C
from time import sleep

show_data = ""


def show_main_menu():
    oled_option.centerText(BME280)
    main_menu.draw()


def show_temp():
    global show_data
    show_data = "temp"
    update_info()
    show_main_menu()


def show_hum():
    global show_data
    show_data = "hum"
    update_info()
    show_main_menu()


def show_press():
    global show_data
    show_data = "press"
    update_info()
    show_main_menu()


def show_all():
    global show_data
    show_data = "all"
    update_info()
    show_main_menu()


def update_info():
    global show_data

    t, h, p = bme.values()

    oled.fill_rect(0, 20, 107, 43, 0)

    if show_data == "temp":
        oled_option.centerText(t, 34)

    elif show_data == "hum":
        oled_option.centerText(h, 34)

    elif show_data == "press":
        oled_option.centerText(p, 34)

    elif show_data == "all":
        oled_option.centerText(t, 24)
        oled_option.centerText(h, 32)
        oled_option.centerText(p, 40)

    oled.show()


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

rotary = Rotary(15, 14, 13)


def rotary_changed(change):
    if change == Rotary.ROT_CCW:
        print("izquierda")
        menu.navigate("left")

    elif change == Rotary.ROT_CW:
        print("derecha")
        menu.navigate("right")

    elif change == Rotary.SW_PRESS:
        print("Seleccionar")
        menu.select()

    elif change == Rotary.SW_RELEASE:
        print('RELEASE')


rotary.add_handler(rotary_changed)

show_all()

while True:
    update_info()
    sleep(0.5)
