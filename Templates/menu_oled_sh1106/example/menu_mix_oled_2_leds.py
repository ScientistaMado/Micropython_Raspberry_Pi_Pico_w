from machine import Pin, I2C
import sh1106
from menuoled import MENU_OPTIONS, MENU_LIST
import time


def show_led_menu():
    print("LED Menu")
    oled.fill(0)
    led_menu.centerText("Menu LED", 0)
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
led_menu = MENU_OPTIONS(oled, y_init=8, partial_update=True)


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

menu = MENU_LIST(menu_list)

# Configura botones de navegación
button_up = Pin(15, Pin.IN, Pin.PULL_DOWN)
button_down = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_select = Pin(13, Pin.IN, Pin.PULL_DOWN)

red_led = Pin(19, Pin.OUT)
green_led = Pin(18, Pin.OUT)

# Dibujar el menú
show_led_menu()

while True:

    if button_up.value():
        print("Arriba")
        menu.navigate("up")
        time.sleep(0.3)

    if button_down.value():
        print("Abajo")
        menu.navigate("down")
        time.sleep(0.3)

    if button_select.value():
        print("Seleccionar")
        menu.select()
        time.sleep(0.3)
