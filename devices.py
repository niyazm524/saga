from enum import Enum
from urllib.request import urlopen, HTTPError, URLError
import os


class DeviceType(Enum):
    DOOR = 1
    ALTAR = 2
    BOARD = 3


class Device:
    device_type = None
    btn_id = None
    name = ""
    actions = []
    IP = None

    def __init__(self, device_type, ip, btn_id=None):
        self.device_type = device_type
        self.IP = "10.0.110."+str(ip)
        self.btn_id = btn_id


class Altar(Device):
    def __init__(self, ip, index, btn_id=None):
        super().__init__(DeviceType.ALTAR, ip, btn_id)
        if index < 1 or index > 5:
            raise Exception("Индекс алтаря - число от 1 до 5")
        self.index = index
        self.name = "Алтарь {}".format(index)

    def send_to_relay(self, command):
        try:
            urlopen("http://{}/relay?bits={}".format(self.IP, command))
        except (HTTPError, URLError):
            return False
        else:
            return True
    
    def turn_off(self):
        t = ["2"]*5
        t[self.index-1] = "0"
        return self.send_to_relay("".join(t))

    def turn_on(self):
        return self.send_to_relay("{:05d}".format(10 ** (self.index-1)))

    def turn_off_all(self):
        return self.send_to_relay("00000")

    def blink_all(self):
        try:
            urlopen("http://{}/blink".format(self.IP))
        except (HTTPError, URLError):
            return False
        else:
            return True


class Board(Device):
    timer = 0
    runes = 0
    name = "Доска"

    def __init__(self, serial):
        super().__init__(DeviceType.BOARD, None)
        self.serial = serial

    def write(self, command):
        os.system("echo {} > {}".format(command, self.serial))

    @staticmethod
    def format_cmd(runes, timer):
        return "2{:02d}2{}".format(runes, timer)

    def set_runes(self, runes):
        self.runes = runes
        self.write(Board.format_cmd(runes, self.timer))

    def set_timer(self, timer):
        self.timer = timer
        self.write(Board.format_cmd(self.runes, timer))

    def set_all(self, runes, timer):
        self.runes = runes
        self.timer = timer
        self.write(Board.format_cmd(runes, timer))

    def start(self):
        self.write("11111")


class Door(Device):
    name = "Дверь"
    from_uart = False
    _is_open = False

    def __init__(self, ip, gpio, index, from_uart=False, btn_id=None):
        super().__init__(DeviceType.DOOR, ip, btn_id)
        self.gpio = gpio
        self.index = index
        self.name = "Дверь {}".format(index)
        self.from_uart = from_uart

    def _format_uart(self, is_open: bool):
        return "uart=20{}0{}".format(self.gpio, int(is_open))

    def _format_esp(self, is_open: bool):
        return "q={}{}".format("OFF" if is_open else "ON", self.gpio)
    @property
    def is_open(self):
        return self._is_open

    @is_open.setter
    def is_open(self, is_open: bool):
        try:
            urlopen("http://{}/?{}".format(self.IP,
                                           self._format_uart(is_open) if self.from_uart else self._format_esp(is_open)))
        except:
            pass

        self._is_open = is_open
