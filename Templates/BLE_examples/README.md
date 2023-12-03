# BLE Simple Peripheral or BLE uart con MicroPython

![Micropython_Raspberry_Pi_Pico_w](https://img.shields.io/badge/Raspberry%20Pi%20Pico%20W-Micropython%20Compatible-brightgreen)


Este código en MicroPython implementa una conexión BLE (Bluetooth Low Energy) simple que actúa como un periférico, que permite controlar el encendido y apagado de un led conectado al pín 15 y envía un mensaje si un botón conectado al pin 14 es presionado

## Requisitos

1. Raspberry Pi Pico W
2. 1 LED
3. 1 resistencia 220 o 330 ohms
4. Pulsador

## Uso

1. Subir a la placa las bibliotecas ble_advertising, ble_simple_peripheral y ble_uart_periferal disponibles en el repositorio
2. Ejecutar el código BLE_send_recieve.py o BLEuart_send_receive.py

## Agradecimientos

Las bibliotecas fueron obtenidas desde el github [MicroPython](https://github.com/micropython)
