from machine import Pin, I2C
import sh1106
from menuoled import MENU_OPTIONS, MENU_LIST
import time


def show_icon_1():
    oled.blit(main_menu.openIcon("person_1"), 70, 0)
    oled.show()
    main_menu.draw()


def show_icon_2():
    oled.blit(main_menu.openIcon("person_2"), 70, 0)
    oled.show()
    main_menu.draw()


def show_icon_3():
    oled.blit(main_menu.openIcon("person_3"), 70, 0)
    oled.show()
    main_menu.draw()


i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = sh1106.SH1106_I2C(128, 64, i2c, rotate=180)

main_menu = MENU_OPTIONS(oled, y_init=10, width_menu=60)

main_menu.add_option("icono 1", show_icon_1)
main_menu.add_option("icono 2", show_icon_2)
main_menu.add_option("icono 3", show_icon_3)

menu_list = [main_menu]

menu = MENU_LIST(menu_list)

# Configura botones de navegación
button_up = Pin(15, Pin.IN, Pin.PULL_DOWN)
button_down = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_select = Pin(13, Pin.IN, Pin.PULL_DOWN)


# Dibujar el menú
oled.text("Main menu:")
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
