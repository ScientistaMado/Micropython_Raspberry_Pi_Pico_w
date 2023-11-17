import framebuf


class DATA_INFO():
    def __init__(self, info_stop_bus):
        self.info_stop_bus = info_stop_bus

        self.id_stop_bus = self.info_stop_bus['id']
        self.name_stop_bus = self.info_stop_bus['name']
        self.status_code = self.info_stop_bus['status_code']
        self.status_description = self.info_stop_bus['status_description']
        self.services = self.info_stop_bus['services']


class SERVICES(DATA_INFO):

    def __init__(self, info_stop_bus):
        super().__init__(info_stop_bus)
        self.n_bus = len(self.services)
        self.bus_in_services_id = self.get_bus_in_services_id()

    def get_bus_in_services_id(self):
        bus_in_services = []

        if self.status_code == 0:
            for service in self.services:
                bus_in_services.append(service['id'])

            return bus_in_services


class BUS(SERVICES):
    def __init__(self, info_stop_bus, id_bus):
        super().__init__(info_stop_bus)
        self.id_bus = id_bus
        self.confirm_id_bus = self.get_confirmation()
        self.valid = self.get_valid()
        self.status_description_bus = self.get_status_description_bus()
        self.buses = self.get_buses()
        self.n_buses = len(self.buses)
        self.info_bus = None

    def get_confirmation(self):
        confirmation = True
        if self.id_bus not in self.bus_in_services_id:
            confirmation = False
        return confirmation

    def get_valid(self):

        for bus in self.services:
            if bus['id'] == self.id_bus:
                return bus['valid']

    def get_status_description_bus(self):
        for bus in self.services:
            if bus['id'] == self.id_bus:
                return bus['status_description']

    def get_buses(self):
        return self.services['buses']

    def get_info_bus(self, n_bus):

        if not self.n_buses:
            return False

        info_bus = {
            'id': self.buses[n_bus]['id'],
            'distance': self.buses[n_bus]['meters_distance'],
            'min_time': self.buses[n_bus]['min_arrival_time'],
            'max_time': self.buses[n_bus]['max_arrival_time']
        }

        self.info_bus = info_bus


class VIEWS():

    def __init__(self, oled):
        self.oled = oled

    def oledCenterText(self, text, y):
        x = int((128 - len(text)*8)/2)
        self.oled.text(text, x, y)

    def openIcon(icon_id):

        with open(f'icons/{icon_id}.pbm', "rb") as file:
            file.readline()
            xy = file.readline()
            x = int(xy.split()[0])
            y = int(xy.split()[1])
            icon = bytearray(file.read())

        return framebuf.FrameBuffer(icon, x, y, framebuf.MONO_HLSB)

    def show_bus(self, bus_id):

        for service in services:
            if service['id'] == bus_id:
                if service['valid']:
                    distance = service['buses'][0]['meters_distance']
                    min_time = service['buses'][0]['min_arrival_time']
                    max_time = service['buses'][0]['max_arrival_time']

                else:
                    print(service["status_description"])
                    self.oled.fill(0)
                    self.oled.text("Sin recorrido", 0, 30)
                    self.oled.show()

        t = f'{min_time}-{max_time} min'
        d = f'{distance} m'

        self.oled.fill(0)

        self.oled.blit(self.openIcon('icon_bus'), 25, 0)
        self.oled.text(id_stop_bus, 50, 0)
        self.oled.text(bus_id, 50, 8)

        self.oledCenterText(d, 25)
        self.oledCenterText(t, 40)

        self.oled.show()
