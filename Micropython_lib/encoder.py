from machine import Pin


class Rotary:
    ROT_CW = 1
    ROT_CCW = 2
    SW_PRESS = 4
    SW_RELEASE = 8

    TRANSITIONS = [0b00, 0b01, 0b11, 0b10, 0b00]

    def __init__(self, dt, clk, sw):
        self.dt_pin = Pin(dt, Pin.IN, Pin.PULL_DOWN)
        self.clk_pin = Pin(clk, Pin.IN, Pin.PULL_DOWN)
        self.sw_pin = Pin(sw, Pin.IN, Pin.PULL_DOWN)
        self.last_status = self.dt_pin.value() << 1 | self.clk_pin.value()
        self.dt_pin.irq(handler=self.rotary_change,
                        trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.clk_pin.irq(handler=self.rotary_change,
                         trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.sw_pin.irq(handler=self.switch_detect,
                        trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.handlers = []
        self.last_button_status = self.sw_pin.value()

    def rotary_change(self, _):
        new_status = self.dt_pin.value() << 1 | self.clk_pin.value()
        transition = self.last_status << 2 | new_status
        if transition in [0b1110, 0b1101]:
            self.call_handlers(self.ROT_CW if transition ==
                               0b1110 else self.ROT_CCW)
        self.last_status = new_status

    def switch_detect(self, _):
        current_button_status = self.sw_pin.value()
        if current_button_status != self.last_button_status:
            self.last_button_status = current_button_status
            self.call_handlers(
                self.SW_RELEASE if current_button_status else self.SW_PRESS)

    def call_handlers(self, event_type):
        try:
            for handler in self.handlers:
                handler(event_type)
        except Exception as e:
            print(f"Error al llamar a los manipuladores: {e}")

    def add_handler(self, handler):
        try:
            self.handlers.append(handler)
        except Exception as e:
            print(f"Error al agregar manipulador: {e}")
