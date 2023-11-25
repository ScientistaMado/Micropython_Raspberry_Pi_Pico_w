# Proyecto MicroPython: Consulta de Paradero y Recorrido a través de consultas a una API

![Micropython_Raspberry_Pi_Pico_w](https://img.shields.io/badge/Raspberry%20Pi%20Pico%20W-Micropython%20Compatible-brightgreen)

Este proyecto está diseñado para funcionar con una placa Raspberry Pi Pico W y permite consultar información sobre el tiempo de espera y la distancia de un bus en un paradero específico. La configuración del paradero y el recorrido se realiza a través de información que se encuentra dentro de un archivo JSON dentro de la placa, que además se puede reconfigurar mediante Bluetooth Low Energy (BLE), y los resultados se muestran en un display OLED.

## Requisitos
Asegúrate de tener los siguientes elementos antes de ejecutar el código:

1. Raspberry Pi Pico W.
2. Módulo OLED SSD1306.
3. Conexión a una red WiFi.
4. Pulsador
5. Botón on off 8x8
6. APP Serial Bluetooth Terminal
7. Bibliotecas, json e íconos
8. Subir el código principal como main.py
   
## Configuración

1. SSID: Nombre de la red WiFi a la que el dispositivo se conectará.
2. PASSWORD: Contraseña de la red WiFi.
3. URL_API: URL de la API que proporciona la información del paradero y el recorrido.

## Funciones Principales

connectWifi(ssid, password)
Esta función establece la conexión a la red WiFi proporcionada.

fetchApi(api_url, stop_bus_id, timeout=15)
Realiza una solicitud HTTP a la API especificada para obtener información sobre el paradero y el recorrido.

showInOled(stop_bus_info, bus_id)
Muestra la información del paradero y el recorrido en el display OLED.

updateInfo()
Actualiza la información consultando la API y muestra los resultados en el display.

config_ble_stop_bus()
Permite la configuración del paradero y el recorrido a través de BLE.

Configuración de Hardware
Conexión de pines para el módulo OLED SSD1306.
Configuración del módulo BLE y su comunicación mediante UART.

## Agradecimientos

Todas las bibliotecas Bluetooth fueron rescatadas del github https://github.com/micropython/micropython/tree/master/examples/bluetooth
