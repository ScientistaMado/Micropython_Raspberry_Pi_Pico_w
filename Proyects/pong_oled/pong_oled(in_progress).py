from machine import Pin, I2C
from sh1106 import SH1106_I2C
from ponglib import FIELD, PLAYER, BALL, GAME
from time import sleep


pot_player_1 = 26
pot_player_2 = 27

i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SH1106_I2C(128, 64, i2c, rotate=180)

field = FIELD(oled)

player_1 = PLAYER(oled, field, pot_player_1, n_player=1)
player_2 = PLAYER(oled, field, pot_player_2, n_player=2)

ball = BALL(oled, field)

pong_game = GAME(oled, field, player_1, player_2, ball)

pong_game.startGame()

button_start = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_reset = Pin(15, Pin.IN, Pin.PULL_DOWN)

while True:
    if button_start.value() and pong_game.in_game == False:
        pong_game.in_game = True
        pong_game.startGame()
    elif button_reset.value() and pong_game.in_game == False:
        pong_game.in_game = True
        pong_game.runGame()
