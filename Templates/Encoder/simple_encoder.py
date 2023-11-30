from machine import Pin
import time
import encoder

rotary = Rotary(14, 15, 13)
val = 0


def rotary_changed(change):
    if change == Rotary.ROT_CW:
        print(1)
    elif change == Rotary.ROT_CCW:
        print(-1)
    elif change == Rotary.SW_PRESS:
        print('PRESS')
    elif change == Rotary.SW_RELEASE:
        print('RELEASE')


rotary.add_handler(rotary_changed)

while True:
    # Your code

    time.sleep(0.1)  # Example waiting
