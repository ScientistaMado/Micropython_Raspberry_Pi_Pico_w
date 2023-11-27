# Test de visualización oled offline

## Consideraciones
El test de visualización de datos en el display oled ssd1306 utiliza el documento example_response.json para simular una consulta a la url API https://api.xor.cl/red/bus-stop/pg335

Debes modificar las líneas

SSID = 'YOUR SSID'     
PASSWORD = 'YOUR PASS'   

Con el nombre y clave de tu red wifi

El ejemplo utiliza en la raspberry pi pico w el puerto I2C 0

SDA en el pin 16
SCL en el pin 17


## Ejecución

Antes de ejecutar el ejemplo en Thonny debes subir a la placa el archivo example_response.json

