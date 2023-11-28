import framebuf


class MENU:

    def __init__(self, oled):
        self.oled = oled
        self.width = oled.width
        self.height = oled.height
        self.justify = {"left": 0, "center": 1, "right": 2}

    def leftText(self, text, y, x_init=None):
        if x_init:
            x = x_init
        else:
            x = 0
        self.oled.text(text, x, y)

    def centerText(self, text, y, x_init=None):
        if x_init:
            x = int((x_init - len(text)*8)/2)
        else:
            x = int((self.width - len(text)*8)/2)

        self.oled.text(text, x, y)

    def rightText(self, text, y, x_init=None):
        if x_init:
            x = int((x_init - len(text)*8))
        else:
            x = int((self.width - len(text)*8))

        self.oled.text(text, x, y)

    def openIcon(self, icon_id):

        with open(f'icons/{icon_id}.pbm', "rb") as file:
            file.readline()
            xy = file.readline()
            x = int(xy.split()[0])
            y = int(xy.split()[1])
            icon = bytearray(file.read())

        return framebuf.FrameBuffer(icon, x, y, framebuf.MONO_HLSB)


class MENU_OPTIONS(MENU):

    def __init__(self, oled, x_init=0, y_init=0, width_menu=128, height_option=8, partial_update=False):
        super().__init__(oled)
        self.options = []
        self.width = width_menu
        self.x_init = x_init
        self.y_init = y_init
        self.height = height_option
        self.in_menu = False
        self.partial_update = partial_update
        self.index_navigate = 0
        self.max_index_navigate = 0
        self.index_select = None

    def add_option(self, text: str, action: callable):
        self.options.append((text, action))
        self.max_index_navigate = len(self.options)-1

    def draw(self, widht=None, height=None):

        if widht == None:
            widht = self.width

        if height == None:
            height = len(self.options)*8

        if self.partial_update:
            self.oled.fill_rect(
                self.x_init, self.y_init, widht, height, 0)
        else:
            self.oled.fill(0)

        self.in_menu = True

        for i, item in enumerate(self.options):
            y = self.y_init + i*8
            if i == self.index_navigate:
                self.on_select(item[0], y)
            else:
                self.oled.text(item[0], self.x_init, y, 1)

        self.oled.show()

    def navigate_up(self):
        self.index_navigate -= 1
        if self.index_navigate < 0:
            self.index_navigate = 0

        if self.max_index_navigate == 0:
            return

        self.draw()

    def navigate_down(self):
        self.index_navigate += 1
        if self.index_navigate >= self.max_index_navigate:
            self.index_navigate = self.max_index_navigate

        if self.max_index_navigate == 0:
            return

        self.draw()

    def on_select(self, text, y):
        self.oled.fill_rect(self.x_init, y, self.width, self.height, 1)
        self.oled.text(text, self.x_init, y, 0)

    def select_option(self):
        self.in_menu = False
        action = self.options[self.index_navigate][1]
        action()


class MENU_LIST():
    def __init__(self, menu_list):
        self.menu_list = menu_list

    def navigate(self, direction: str):

        for menu in self.menu_list:
            if menu.in_menu:
                if direction == "up":
                    menu.navigate_up()
                    print(menu.index_navigate)
                elif direction == "down":
                    menu.navigate_down()
                    print(menu.index_navigate)
                else:
                    print("error de navegación")

    def select(self):

        for menu in self.menu_list:
            if menu.in_menu:
                menu.select_option()
                return
