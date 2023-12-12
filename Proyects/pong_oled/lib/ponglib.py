from machine import ADC
from math import sin, cos, radians
from time import sleep


class FIELD:
    def __init__(self, oled, score_p1=0, score_p2=0, x_init_field=0, y_init_field=8, font_size=8):
        self.oled = oled
        self.font_size = font_size
        self.score_p1 = score_p1
        self.score_p2 = score_p2
        self.score = f'P1 {self.score_p1} | {self.score_p2} P2'
        self.y_init_field = y_init_field
        self.x_init_field = x_init_field
        self.x_end_field = self.oled.width - 2*self.x_init_field
        self.width_play_field = self.x_end_field - self.x_init_field
        self.height_play_field = self.oled.height - self.y_init_field
        self.y_end_field = self.y_init_field + self.height_play_field
        self.drawScreen()

    def updateScore(self):
        self.score = f'P1 {self.score_p1} | {self.score_p2} P2'
        self.oled.fill_rect(0, 0, self.oled.width, self.font_size, 0)
        x = ((self.oled.width-len(self.score)*self.font_size)//2)
        self.oled.text(str(self.score), x, 1)

    def drawScreen(self):
        # self.oled.hline(0, self.y_init_field-1, self.oled.width, 1)
        self.updateScore()
        self.oled.show()


class PLAYER:
    def __init__(self, oled, field, pin_player, long=2, thickness=2, n_player=1):
        self.oled = oled
        self.field = field
        self.long = self.getLong(long)
        self.min_y = self.field.y_init_field
        self.pos_y_top = self.field.y_init_field
        self.pos_y_bottom = self.pos_y_top + self.long
        self.thickness = thickness
        self.n_player = n_player
        self.pos_x = self.getPosX()
        self.pin_player = ADC(pin_player)

        self.updatePosY()
        self.updatePosPlayer()

    def getLong(self, init_long):
        if init_long in range(1, 4):
            long = init_long * 8
        else:
            raise ValueError("El largo del jugador solo puede ser 1, 2 o 3")
        return long

    def getPosX(self):

        if self.n_player == 1:
            init_pos_x = self.field.x_init_field
        elif self.n_player == 2:
            init_pos_x = self.field.x_end_field - self.thickness
        else:
            raise ValueError(
                f"Número de jugador inválido: {self.n_player}")

        return init_pos_x

    def clamp(self, value, minimum, maximum):
        return max(minimum, min(value, maximum))

    def updatePosY(self):
        pot_read = self.pin_player.read_u16()

        pos_y = int((pot_read/65535)*self.field.height_play_field) + \
            self.field.y_init_field

        pos_y = self.clamp(pos_y, self.min_y, self.min_y +
                           self.field.height_play_field - self.long)

        self.pos_y_top = pos_y
        self.pos_y_bottom = pos_y + self.long

    def updatePosPlayer(self):
        self.updatePosY()
        x = self.pos_x
        self.oled.fill_rect(x, self.pos_y_top, self.thickness, self.long, 1)


class BALL:
    def __init__(self, oled, field, radio=2, direction=45, vel=4):
        self.oled = oled
        self.field = field

        self.pos_x = self.oled.width//2
        self.pos_y = (self.field.height_play_field//2)+self.field.y_init_field
        self.radio = radio

        self.max_y = self.getMaxY()
        self.max_x = self.getMaxX()

        self.direction = direction
        self.vel = vel

    def initBall(self):
        self.pos_x = self.oled.width//2
        self.pos_y = (self.field.height_play_field//2)+self.field.y_init_field

    def getMaxY(self):
        return self.pos_y + self.radio

    def getMaxX(self):
        return self.pos_x + self.radio

    def drawBall(self, x, y, r):
        self.oled.fill_rect(x, y, r, r, 1)

    def updatePosBall(self):
        self.pos_x += int(self.vel*cos(radians(self.direction)))

        self.pos_y += int(self.vel*sin(radians(self.direction)))

        self.drawBall(self.pos_x, self.pos_y, self.radio)


class GAME:
    def __init__(self, oled, field, player_1, player_2, ball):
        self.oled = oled

        self.field = field
        self.x_min = self.field.x_init_field
        self.y_min = self.field.y_init_field
        self.w_field = self.field.width_play_field
        self.h_field = self.field.height_play_field
        self.x_max = self.field.x_end_field
        self.y_max = self.field.y_end_field

        self.player_1 = player_1
        self.player_2 = player_2

        self.ball = ball

        self.in_game = True

    def clamp(self, value, minimum, maximum):
        return max(minimum, min(value, maximum))

    def colisionBall(self):

        # Colisión con los límites verticales del campo
        if self.ball.pos_y <= self.y_min or self.ball.getMaxY() >= self.y_max:
            self.ball.direction = 360 - self.ball.direction  # Rebote vertical

        # Colisión con el jugador 1
        elif self.ball.pos_x <= self.player_1.pos_x + self.player_1.thickness:
            if self.player_1.pos_y_top <= self.ball.pos_y <= self.player_1.pos_y_bottom:
                self.ball.pos_x = self.player_1.pos_x + self.player_1.thickness
                self.ball.direction = 180 - self.ball.direction  # Rebote horizontal
            else:
                self.field.score_p2 += 1
                self.stopGame()

        # Colisión con el jugador 2
        elif self.ball.pos_x >= self.player_2.pos_x:

            if self.player_2.pos_y_top <= self.ball.pos_y <= self.player_2.pos_y_bottom:
                self.ball.pos_x = self.player_2.pos_x - \
                    self.player_2.thickness - self.ball.radio
                self.ball.direction = 180 - self.ball.direction  # Rebote horizontal
            else:
                self.field.score_p1 += 1
                self.stopGame()

    def updateField(self):
        self.oled.fill_rect(self.x_min, self.y_min,
                            self.w_field, self.h_field, 0)

        self.player_1.updatePosPlayer()
        self.player_2.updatePosPlayer()
        self.ball.updatePosBall()

        self.colisionBall()
        self.oled.show()

    def updateGameScore(self):
        self.field.updateScore()
        self.oled.show()

    def runGame(self):
        self.ball.initBall()
        self.ball.direction = 45
        while self.in_game:
            self.updateField()
            sleep(0.05)

    def stopGame(self):
        self.in_game = False
        self.updateGameScore()

    def startGame(self):
        self.field.score_p1 = 0
        self.field.score_p2 = 0
        self.updateGameScore()
        self.runGame()
