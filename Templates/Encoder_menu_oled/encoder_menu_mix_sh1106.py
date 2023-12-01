from machine import Pin, I2C
import sh1106
from encoder import Rotary
from menuoled import MENU, MENU_OPTIONS, NAVIGATE_MENU
import time


def show_led_menu():
    print("LED Menu")

    oled.fill(0)
    menu_extras.centerText("Control LED", 0)
    oled.show()

    led_menu.draw()


def show_red_led_menu():
    print("Red LED menu")

    oled.fill(0)
    menu_extras.centerText("Control Red LED", 0)

    if red_led.value():
        oled.blit(menu_extras.openIcon("led_on_2"), 80, 16)
    else:
        oled.blit(menu_extras.openIcon("led_off_2"), 80, 16)

    oled.show()

    red_led_menu.draw()


def show_blue_led_menu():
    print("Red LED menu")

    oled.fill(0)
    menu_extras.centerText("Control Blue LED", 0)

    if blue_led.value():
        oled.blit(menu_extras.openIcon("led_on_2"), 80, 16)
    else:
        oled.blit(menu_extras.openIcon("led_off_2"), 80, 16)

    oled.show()

    blue_led_menu.draw()


def red_led_on():
    red_led.value(1)
    print("Red LED On")
    show_red_led_menu()


def red_led_off():
    red_led.value(0)
    print("Red LED Off")
    show_red_led_menu()


def blue_led_on():
    blue_led.value(1)
    print("blue LED On")
    show_blue_led_menu()


def blue_led_off():
    blue_led.value(0)
    print("blue LED Off")
    show_blue_led_menu()


# Crear un OLED
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = sh1106.SH1106_I2C(128, 64, i2c, rotate=180)


# Crear un menú principal
led_menu = MENU_OPTIONS(oled, y_init=16, width_menu=66, partial_update=True)


# Agregar elementos a led_menu
led_menu.add_option("Blue LED", show_blue_led_menu)
led_menu.add_option("Red LED", show_red_led_menu)


# Crea menú red_led_menu
red_led_menu = MENU_OPTIONS(
    oled, y_init=16, width_menu=66, partial_update=True)


# Agregar elementos a red_led_menu
red_led_menu.add_option("LED menu", show_led_menu)
red_led_menu.add_option("LED on", red_led_on)
red_led_menu.add_option("LED off", red_led_off)


# Crea menú blue_led_menu
blue_led_menu = MENU_OPTIONS(
    oled, y_init=16, width_menu=66, partial_update=True)


# Agregar elementos a red_led_menu
blue_led_menu.add_option("LED menu", show_led_menu)
blue_led_menu.add_option("LED on", blue_led_on)
blue_led_menu.add_option("LED off", blue_led_off)


menu_list = [led_menu,
             red_led_menu,
             blue_led_menu,
             ]

menu = NAVIGATE_MENU(menu_list)

menu_extras = MENU(oled)
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


red_led = Pin(11, Pin.OUT)
blue_led = Pin(12, Pin.OUT)

# Dibujar el menú
show_led_menu()

rotary.add_handler(rotary_changed)
