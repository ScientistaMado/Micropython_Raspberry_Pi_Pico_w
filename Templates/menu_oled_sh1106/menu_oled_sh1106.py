from machine import Pin, I2C
import sh1106
from menuoled import MENU_OPTIONS, MENU_LIST
import time


def show_main_menu():
    print("Menú principal")
    main_menu.draw()


def option_1():
    print("Opción 1 seleccionada")
    secondary_menu.draw()


def simple_text():
    print("Opción 2 seleccionada")

    simple_text_menu.draw()
    oled.text("Esta es la opcion", 0, 16)
    oled.text("de texto simple", 0, 24)
    oled.show()


def show_icon():
    print("Opción 3 seleccionada")

    show_icon_menu.draw()
    oled.blit(show_icon_menu.openIcon('config'), 20, 16)
    oled.show()


def option_1_1():
    print("Opción 1_1 seleccionada")
    option_1_1_menu.draw()
    oled.text("NADA", 30, 18)
    oled.show()


# Crear un OLED
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = sh1106.SH1106_I2C(128, 64, i2c, rotate=180)

# Crear un menú principal
main_menu = MENU_OPTIONS(oled)

# Agregar elementos a main_menu
main_menu.add_option("Menu secundario", option_1)
main_menu.add_option("Texto simple", simple_text)
main_menu.add_option("Icono", show_icon)


# Crea menú de la opción 1
secondary_menu = MENU_OPTIONS(oled)

# Agregar elementos a menu_option_1
secondary_menu.add_option("Menu principal", show_main_menu)
secondary_menu.add_option("Opcion 1.1", option_1_1)


# Crea menú de la opción texto simple
simple_text_menu = MENU_OPTIONS(oled)

# Agregar elementos a texto simple
simple_text_menu.add_option("Menu principal", show_main_menu)


show_icon_menu = MENU_OPTIONS(oled)

# Agregar elementos a texto simple
show_icon_menu.add_option("Menu principal", show_main_menu)


option_1_1_menu = MENU_OPTIONS(oled)

# Agregar elementos a texto simple
option_1_1_menu.add_option("Menu principal", show_main_menu)


menu_list = [main_menu,
             secondary_menu,
             simple_text_menu,
             show_icon_menu,
             option_1_1_menu]

menu = MENU_LIST(menu_list)

# Configura botones de navegación
button_down = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_up = Pin(13, Pin.IN, Pin.PULL_DOWN)
button_select = Pin(15, Pin.IN, Pin.PULL_DOWN)


# Dibujar el menú
main_menu.draw()

while True:

    if button_up.value():
        print("Arriba")
        menu.navigate("up")
        time.sleep(0.5)

    if button_down.value():
        print("Abajo")
        menu.navigate("down")
        time.sleep(0.5)

    if button_select.value():
        print("Seleccionar")
        menu.select()
        time.sleep(0.5)
