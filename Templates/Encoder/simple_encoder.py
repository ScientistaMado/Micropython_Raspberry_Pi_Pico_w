from machine import Pin
import time
from encoder import Rotaray

# Rotary(dt, clk, sw) pin number only
rotary = Rotary(14, 15, 13)


# Function that will be executed when there is a change in the encoder
def rotary_changed(change):
    if change == Rotary.ROT_CW:
        print(1)
    elif change == Rotary.ROT_CCW:
        print(-1)
    elif change == Rotary.SW_PRESS:
        print('PRESS')
    elif change == Rotary.SW_RELEASE:
        print('RELEASE')


# Attaches rotary_changed function to rotary object
rotary.add_handler(rotary_changed)

while True:
    # Your code

    time.sleep(0.1)  # Example waiting
