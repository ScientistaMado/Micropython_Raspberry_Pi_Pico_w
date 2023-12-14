from machine import Pin, I2C
from sh1106 import SH1106_I2C
from ponglib import FIELD, PLAYER, BALL, GAME


pot_player_1 = 26   # Pin ADC0
pot_player_2 = 27   # Pin ADC1

i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SH1106_I2C(128, 64, i2c, rotate=180)

# Crea el campo de juego
field = FIELD(oled)

# Crea los jugadores
player_1 = PLAYER(oled, field, pot_player_1, n_player=1)
player_2 = PLAYER(oled, field, pot_player_2, n_player=2)

# Crea la pelota
ball = BALL(oled, field)

# Unifica los objetos en un juego
pong_game = GAME(oled, field, player_1, player_2, ball)

# Configura los pulsadores
button_start = Pin(14, Pin.IN, Pin.PULL_DOWN)  # Reinicia el puntaje
button_continue = Pin(15, Pin.IN, Pin.PULL_DOWN)  # Continua con el puntaje

# Muestra imagen de inicio
pong_game.showImageIntro("pong_intro")


while not (button_start.value() or button_continue.value()):
    pass

pong_game.in_game = True
pong_game.startGame()

while True:
    if button_start.value() and pong_game.in_game == False:
        pong_game.in_game = True
        pong_game.startGame()
    elif button_continue.value() and pong_game.in_game == False:
        pong_game.in_game = True
        pong_game.runGame()
