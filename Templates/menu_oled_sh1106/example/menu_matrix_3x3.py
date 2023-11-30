from machine import Pin, I2C
import sh1106
from menuoled import MENU_ICONS, NAVIGATE_MENU
import time


def show_main_menu():
    print("Menú principal")
    main_menu.draw()


i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = sh1106.SH1106_I2C(128, 64, i2c, rotate=180)


main_menu = MENU_ICONS(oled, n_icons_x=3, n_icons_y=3)

main_menu.add_option("1", show_main_menu, 0, 0)
main_menu.add_option("2", show_main_menu, 1, 0)
main_menu.add_option("3", show_main_menu, 2, 0)

main_menu.add_option("1", show_main_menu, 0, 1)
main_menu.add_option("2", show_main_menu, 1, 1)
main_menu.add_option("3", show_main_menu, 2, 1)

main_menu.add_option("1", show_main_menu, 0, 2)
main_menu.add_option("2", show_main_menu, 1, 2)
main_menu.add_option("3", show_main_menu, 2, 2)


menu_list = [main_menu]

menu = NAVIGATE_MENU(menu_list)

# Configura botones de navegación
button_up = Pin(15, Pin.IN, Pin.PULL_DOWN)
button_down = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_select = Pin(13, Pin.IN, Pin.PULL_DOWN)
button_right = Pin(12, Pin.IN, Pin.PULL_DOWN)
button_left = Pin(11, Pin.IN, Pin.PULL_DOWN)


# Dibujar el menú
main_menu.draw()

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

    if button_left.value():
        print("izquierda")
        menu.navigate("left")
        time.sleep(0.3)

    if button_right.value():
        print("derecha")
        menu.navigate("right")
        time.sleep(0.3)
