from machine import Pin, I2C
from menuoled import MENU, MENU_ICONS, NAVIGATE_MENU
from bme280 import BME280
from encoder import Rotary
from sh1106 import SH1106_I2C
from time import sleep
import ubuntu_15


def show_main_menu():
    oled.text("BME", 98, 0)
    oled.text("280", 98, 8)
    main_menu.draw()


def show_temp():
    menu_extras.internal_var = "temp"
    show_main_menu()
    update_info()


def show_hum():
    menu_extras.internal_var = "hum"
    show_main_menu()
    update_info()


def show_press():
    menu_extras.internal_var = "press"
    show_main_menu()
    update_info()


def show_all():
    menu_extras.setInternalVar("all")
    show_main_menu()
    update_info()


def update_info():
    t, p, h = bme.values

    oled.fill_rect(0, 20, 127, 43, 0)

    if menu_extras.internal_var == "temp":
        menu_extras.text("Temperatura", 20, 20)
        menu_extras.text(t, 40, 38)
        # oled_option.centerText(t, 34)

    elif menu_extras.internal_var == "hum":
        menu_extras.text("Humedad", 32, 20)
        menu_extras.text(h, 40, 38)
        # oled_option.centerText(h, 34)

    elif menu_extras.internal_var == "press":
        menu_extras.text("Presion", 40, 20)
        menu_extras.text(p, 30, 38)
        # oled_option.centerText(p, 34)

    elif menu_extras.internal_var == "all":
        oled.text(f'Temp: {t}', 5, 24)
        oled.text(f'Hum:  {h}', 5, 34)
        oled.text(f'Pres: {p}', 5, 44)

    oled.show()


i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SH1106_I2C(128, 64, i2c, rotate=180)

bme = BME280(i2c=i2c)

main_menu = MENU_ICONS(oled, n_icons_x=4, n_icons_y=1, separate=3)

main_menu.add_option("temperatura", show_temp, 0, 0)
main_menu.add_option("humedad", show_hum, 1, 0)
main_menu.add_option("presion", show_press, 2, 0)
main_menu.add_option("todo", show_all, 3, 0)

# oled_option = MENU(oled)

menu_list = [main_menu]

menu = NAVIGATE_MENU(menu_list)

menu_extras = MENU(oled)
menu_extras.setFont(ubuntu_15)

rotary = Rotary(11, 12, 13)


def rotary_changed(change):
    if change == Rotary.ROT_CCW:
        print("izquierda")
        menu.navigate("left")

    elif change == Rotary.ROT_CW:
        print("derecha")
        menu.navigate("right")


def button_changed(change):

    if change == Rotary.SW_PRESS:
        print("Seleccionar")
        menu.select()

    elif change == Rotary.SW_RELEASE:
        print('RELEASE')


rotary.add_handler(rotary_changed)
rotary.add_handler(button_changed)


show_all()

while True:
    update_info()
    sleep(10)
