from enum import Enum
from urllib.request import urlopen, HTTPError, URLError
import os


class DeviceType(Enum):
    DOOR = 1
    ALTAR = 2


class Device:
    device_type = None
    IP = None

    def __init__(self, device_type, ip):
        self.device_type = device_type
        self.IP = ip


class Altar(Device):
    def __init__(self, ip, index):
        super().__init__(DeviceType.ALTAR, ip)
        if index < 1 or index > 5:
            raise Exception("Индекс алтаря - число от 1 до 5")
        self.index = index

    def send_command(self, command):
        try:
            urlopen("http://{}/index.php?uart={}".format(self.IP, command))
        except (HTTPError, URLError):
            return False
        else:
            return True

    def turn_off(self):
        return self.send_command("20{}00".format(self.index))

    def turn_on(self):
        return self.send_command("20{}01".format(self.index))

    def turn_off_all(self):
        return self.send_command("30000")

    def blink_all(self):
        return self.send_command("11111")