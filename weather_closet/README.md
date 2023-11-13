# Recomendador de ropa Micropython Raspberry Pi Pico W

![Micropython_Raspberry_Pi_Pico_w](https://img.shields.io/badge/Raspberry%20Pi%20Pico%20W-Micropython%20Compatible-brightgreen)

![ESP8266](https://img.shields.io/badge/ESP8266-Compatible-blue)

Este proyecto es un ejemplo de una aplicación que obtiene datos de pronóstico del tiempo de una API y muestra la información en una pantalla OLED en un dispositivo basado en el microcontrolador ESP8266.

## Requisitos

- Raspberry Pi Pico W
- Pantalla OLED SH1106
- 2 Registros de desplazamiento 74hc595 o 74hc595n
- Shield 18650 de una celda
- Una bateria 18650
- Placas PCB perforadas
- Conexión a Internet
- Modelos 3D impresos Closet_bottom y Closet_frontis de la carpeta Diseños 3D

## Configuración

Antes de usar la aplicación, asegúrate de configurar los siguientes parámetros en el código:

- `SSID`: Nombre de tu red Wi-Fi.
- `PASSWORD`: Contraseña de tu red Wi-Fi.
- `URL_API`: URL de la API del pronóstico del tiempo.

Asegúrate de haber conectado físicamente tu dispositivo al hardware correspondiente, como la pantalla OLED y los pines I2C, según las conexiones en el código.

## Uso

1. Debes subir a tu placa NodeMCU 8266 los archivos weather_closet.py renombrándolo como main.py para que pueda ser ejecutado al iniciar la placa

2. Para controlar el display oled y los led se requiere que subas la carpeta lib a la placa

3. Para que la pantalla oled pueda mostrar los íconos debes crear en la placa una carpeta que se llame 'icons' y solo subir los archivos que se encuentran dentro de la carpeta icons/pbm.

4. El código se encarga de conectarse a tu red Wi-Fi proporcionando las credenciales (`SSID` y `PASSWORD`) y luego obtiene datos del pronóstico del tiempo desde la API definida en `URL_API`. Puedes obtener el link a la API registrándote en https://www.meteored.cl/api/

2. Los datos del pronóstico del tiempo se muestran en la pantalla OLED, incluyendo el día de la semana, temperaturas mínimas y máximas, y un ícono que representa el estado del tiempo.

3. Además, el código también interactúa con un sistema de administración de ropa (`ClothingManager`) para sugerir un atuendo adecuado según el pronóstico del tiempo.

## Personalización

Puedes personalizar este código agregando modificando la biblioteca `ClothingManager` ajustando la forma en que se sugiere el atuendo de acuerdo a tus preferencias personales.

## Créditos

Este código utiliza las bibliotecas de micropython para interactuar con la pantalla OLED de robert-hh y la API del pronóstico del tiempo de Meteored.cl.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
