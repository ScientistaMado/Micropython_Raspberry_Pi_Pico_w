from machine import Pin, I2C
import sh1106
from encoder import Rotary
from menuoled import MENU_OPTIONS, NAVIGATE_MENU
import time


def show_led_menu():
    print("LED Menu")
    led_menu.draw()


def show_red_led_menu():
    print("Red LED menu")
    red_led_menu.draw()


def show_green_led_menu():
    print("Red LED menu")
    green_led_menu.draw()


def red_led_on():
    red_led.value(1)
    print("Red LED On")
    red_led_menu.draw()


def red_led_off():
    red_led.value(0)
    print("Red LED Off")
    red_led_menu.draw()


def green_led_on():
    green_led.value(1)
    print("Green LED On")
    green_led_menu.draw()


def green_led_off():
    green_led.value(0)
    print("Green LED Off")
    green_led_menu.draw()


# Crear un OLED
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = sh1106.SH1106_I2C(128, 64, i2c, rotate=180)


# Crear un menú principal
led_menu = MENU_OPTIONS(oled)


# Agregar elementos a led_menu
led_menu.add_option("Red LED", show_red_led_menu)
led_menu.add_option("Green LED", show_green_led_menu)


# Crea menú red_led_menu
red_led_menu = MENU_OPTIONS(oled)


# Agregar elementos a red_led_menu
red_led_menu.add_option("LED menu", show_led_menu)
red_led_menu.add_option("LED on", red_led_on)
red_led_menu.add_option("LED off", red_led_off)


# Crea menú green_led_menu
green_led_menu = MENU_OPTIONS(oled)


# Agregar elementos a red_led_menu
green_led_menu.add_option("LED menu", show_led_menu)
green_led_menu.add_option("LED on", green_led_on)
green_led_menu.add_option("LED off", green_led_off)


menu_list = [led_menu,
             red_led_menu,
             green_led_menu,
             ]

menu = NAVIGATE_MENU(menu_list)

# Configura encoder de navegación
# Rotary(dt, clk, sw) pin number only
rotary = Rotary(15, 14, 13)


def rotary_changed(change):
    if change == Rotary.ROT_CCW:
        print("Arriba")
        menu.navigate("up")

    elif change == Rotary.ROT_CW:
        menu.navigate("down")
        print("Abajo")

    elif change == Rotary.SW_PRESS:
        print("Seleccionar")
        menu.select()

    elif change == Rotary.SW_RELEASE:
        print('RELEASE')


red_led = Pin(19, Pin.OUT)
green_led = Pin(18, Pin.OUT)

# Dibujar el menú
show_led_menu()

rotary.add_handler(rotary_changed)
