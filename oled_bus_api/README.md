# Proyecto Micropython para Raspberry Pi Pico W

Este proyecto utiliza una Raspberry Pi Pico W programada con MicroPython para obtener información en tiempo real sobre la llegada de buses en un paradero específico. La información se obtiene a través de una API y se muestra en un display OLED. El código está diseñado para ser ejecutado en entornos como Visual Studio Code (VSCode) con soporte para MicroPython.

## Configuración
Antes de ejecutar el código, asegúrate de configurar los siguientes parámetros:

Red WiFi: Configura el nombre de tu red WiFi (SSID) y la contraseña correspondiente en las variables SSID y PASSWORD.
python

SSID = 'TU_RED_WIFI'
PASSWORD = 'TU_CONTRASEÑA'

##Instalación
1. Instala MicroPython en tu Raspberry Pi Pico W
2. Carga el código en tu Raspberry Pi Pico W
3. Carga las carpetas [lib](/lib/) y [icons](/icons/) a la Raspberry Pi Pico W

## Personalización
1. Para cambiar el paradero que deseas consultar, modifica el valor de la variable stop_bus en la llamada a la función fetchApiBus.

data = fetchApiBus(URL_API, 'PG335')

2. Para consultar información sobre un recorrido específico, modifica el valor del segundo argumento en la llamada a la función showInOled.

showInOled(data, '229')

## Dependencias
Este proyecto utiliza las siguientes bibliotecas de MicroPython:

network: Para gestionar la conexión a la red WiFi.
gc: Para la recolección de basura.
time: Para manejar el tiempo.
urequests (alias requests): Para realizar solicitudes HTTP.
ssd1306: Para controlar el display OLED.
framebuf: Para trabajar con imágenes.
json: Para manipular archivos JSON.
machine: Para utilizar pines y la interfaz I2C.
Contribuciones
Siéntete libre de contribuir al proyecto. ¡Esperamos tus sugerencias y mejoras!

Nota: Asegúrate de tener todas las dependencias instaladas en tu entorno de desarrollo antes de ejecutar el código.

## Agradecimientos
La biblioteca ssd1306 es de josh-wawico [linka a su github](https://github.com/makerportal/rpi-pico-ssd1306/blob/main/micropython/data_display/ssd1306.py)
