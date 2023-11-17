from machine import Pin
import utime

class Encoder:
    def __init__(self, pin_a, pin_b):
        self.pin_a = Pin(pin_a, Pin.IN)
        self.pin_b = Pin(pin_b, Pin.IN)
        self.counter = 0
        self.prev_state = 0
        self.pin_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.callback)
        self.pin_b.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.callback)

    def callback(self, pin):
        a = self.pin_a.value()
        b = self.pin_b.value()
        state = (a << 1) | b
        change = (self.prev_state << 2) | state
        if change == 0b1101 or change == 0b0100 or change == 0b0010 or change == 0b1011:
            self.counter += 1
        elif change == 0b1110 or change == 0b0111 or change == 0b0001 or change == 0b1000:
            self.counter -= 1
        self.prev_state = state

    def get_count(self):
        return self.counter

# Configura los pines del encoder
PIN_A = 15  # Reemplaza con el número de pin adecuado
PIN_B = 14  # Reemplaza con el número de pin adecuado

# Crea una instancia del objeto Encoder
encoder = Encoder(PIN_A, PIN_B)

current_count = 0
while True:
    new_count = encoder.get_count()
    
    if new_count % 4 == 0 and new_count != current_count:
        current_count = int(new_count/4)
        print(f'Contador: {current_count}')
        utime.sleep_ms(100)
        