from machine import Pin, I2C
import sh1106
from menuoled import MENU_OPTIONS, MENU_LIST
import time


def show_box():
    oled.blit(main_menu.openIcon("box"), 80, 15)
    oled.show()
    main_menu.draw()


def show_icon_1():
    oled.blit(main_menu.openIcon("person_1"), 80, 0)
    oled.show()
    main_menu.draw()


def show_icon_2():
    oled.blit(main_menu.openIcon("person_2"), 80, 0)
    oled.show()
    main_menu.draw()


def show_icon_3():
    oled.blit(main_menu.openIcon("person_3"), 80, 0)
    oled.show()
    main_menu.draw()


def show_main_menu():
    oled.fill(0)
    oled.text("Main menu:", 0, 0)
    main_menu.draw()


def show_menu_weather():
    oled.fill(0)
    oled.text("Weather menu:", 0, 0)
    weather_menu.draw()


def show_icon_w_sun():
    oled.blit(weather_menu.openIcon("sun"), 80, 15)
    oled.show()
    weather_menu.draw()


def show_icon_w_rain():
    oled.blit(weather_menu.openIcon("rain"), 80, 15)
    oled.show()
    weather_menu.draw()


def show_icon_w_cloudy():
    oled.blit(weather_menu.openIcon("cloudy"), 80, 15)
    oled.show()
    weather_menu.draw()


i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = sh1106.SH1106_I2C(128, 64, i2c, rotate=180)


main_menu = MENU_OPTIONS(oled, y_init=10, width_menu=60, partial_update=True)

main_menu.add_option("Box", show_box)
main_menu.add_option("icono 1", show_icon_1)
main_menu.add_option("icono 2", show_icon_2)
main_menu.add_option("icono 3", show_icon_3)
main_menu.add_option("Weather", show_menu_weather)


weather_menu = MENU_OPTIONS(
    oled, y_init=10, width_menu=75, partial_update=True)

weather_menu.add_option("Sun", show_icon_w_sun)
weather_menu.add_option("Rain", show_icon_w_rain)
weather_menu.add_option("cloudy", show_icon_w_cloudy)
weather_menu.add_option("Main menu", show_main_menu)


menu_list = [main_menu, weather_menu]

menu = MENU_LIST(menu_list)

# Configura botones de navegación
button_up = Pin(15, Pin.IN, Pin.PULL_DOWN)
button_down = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_select = Pin(13, Pin.IN, Pin.PULL_DOWN)


# Dibujar el menú
show_main_menu()

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
