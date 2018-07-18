from enum import Enum
from urllib.request import urlopen, HTTPError, URLError
import os


class DeviceType(Enum):
    DOOR = 1
    ALTAR = 2
    BOARD = 3
    TRUNKS = 4
    BARREL = 5
    TREE = 6
    EQUALIZER = 7


class Device:
    device_type = None
    control = None
    actions = []
    btn_id = None
    name = ""
    IP = None

    def __init__(self, device_type, ip, btn_id=None):
        self.device_type = device_type
        self.IP = "10.0.110."+str(ip)
        self.btn_id = btn_id


class Altars(Device):
    _actived = 0

    def __init__(self, ip):
        super().__init__(DeviceType.ALTAR, ip)
        self.name = "Алтари"

    def send(self, command):
        try:
            urlopen("http://{}/set?n={}".format(self.IP, command))
            print("http://{}/set?n={}".format(self.IP, command))
        except (HTTPError, URLError):
            return False
        else:
            return True

    @property
    def actived(self):
        return self._actived

    @actived.setter
    def actived(self, activate):
        if 0 <= activate <= 5:
            self.send(activate)

    def turn_off_all(self):
        return self.send(0)

    def blink_all(self):
        self.send(6)


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
    url_to_open = ""
    url_to_close = ""
    url_to_activate = ""
    url_to_deactivate = ""
    can_deactivate = False
    _is_open = False

    def __init__(self, ip, cls_type="Дверь", index="", btn_id=None, can_activate=False):
        super().__init__(DeviceType.DOOR, ip)
        self.name = "{} {}".format(cls_type, index)
        if btn_id is None:
            self.btn_id = "door{}".format(index)
        else:
            self.btn_id = btn_id
        self.can_activate = can_activate

    @property
    def is_open(self):
        return self._is_open

    def activate(self):
        try:
            urlopen(self.url_to_activate)
        except:
            pass

    def deactivate(self):
        if self.url_to_deactivate == "":
            return
        try:
            urlopen(self.url_to_deactivate)
        except:
            pass

    @is_open.setter
    def is_open(self, is_open: bool):
        try:
            urlopen(self.url_to_open if is_open else self.url_to_close)
        except:
            pass

        self._is_open = is_open


class EspDoor(Door):
    def __init__(self, ip, gpio, index=0, m=0, cls_type="Дверь", btn_id=None):
        super().__init__(ip, index=index, can_activate=(m != 0), cls_type=cls_type, btn_id=btn_id)
        self.url_to_open = "http://{}/?q={}{}".format(ip, "OFF", gpio)
        self.url_to_close = "http://{}/?q={}{}".format(ip, "ON", gpio)
        self.url_to_activate = "http://{}/?m={}".format(self.IP, m)


class UartDoor(Door):
    def __init__(self, ip, gpio, index=0, cls_type="Дверь", btn_id=None):
        super().__init__(ip, index=index, can_activate=True, cls_type=cls_type, btn_id=btn_id)
        self.url_to_open = "http://{}/?uart=20{}0{}".format(ip, gpio, 0)
        self.url_to_close = "http://{}/?uart=20{}0{}".format(ip, gpio, 1)
        self.url_to_activate = "http://{}/?{}".format(self.IP, "u=11111")


class PhpDoor(Door):
    def __init__(self, ip, cls_type="Дверь", btn_id=None):
        super().__init__(ip, index="", can_activate=True, cls_type=cls_type, btn_id=btn_id)
        self.url_to_open = "http://{}/?relay1={}".format(ip, "off")
        self.url_to_close = "http://{}/?relay1={}".format(ip, "on")
        self.url_to_activate = "http://{}/?script={}".format(ip, "on")
        self.url_to_deactivate = "http://{}/?script={}".format(ip, "off")
        self.can_deactivate = True


class Tree(Door):
    def __init__(self, ip, btn_id):
        super().__init__(ip, cls_type="Древо", btn_id=btn_id, can_activate=True)
        self.url_to_open = "http://{}/off".format(ip)
        self.url_to_close = "http://{}/on".format(ip)
        self.url_to_activate = "http://{}/start".format(ip)
        self.url_to_deactivate = "http://{}/stop".format(ip)



