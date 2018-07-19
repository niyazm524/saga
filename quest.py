import threading
import logging, logging.config
from configs.log_config import log_config
from events import Event, EventType
from player import Player
import configs.device_config as devices
import time
from enum import Enum
from threading import Timer


class Progress(Enum):
    JUST_STARTED = 0
    PASSED_ALTAR1 = 1
    PASSED_TRUNKS = 2
    PASSED_RFID = 3
    PASSED_EQUALIZER = 4
    PASSED_TREE = 5
    PASSED_BARREL = 6


class Quest:
    quit = False
    start_time = None
    timer = None
    observer = None
    _fulltime_minutes = 90
    in_process = False
    progress = Progress.JUST_STARTED
    trunk_index = 0
    trunks_right = [2, 3, 4, 5, 6, 7]
    _aro = 0

    def __init__(self, name, player: Player):
        # threading.Thread.__init__(self)
        # self.daemon = True
        self.name = name
        self.player = player
        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger("quest")
        self.logger.info("Quest {} initiated".format(self.name))

    def update(self, event):
        if event.event_type == EventType.QUEST_START:
            self.legend()
        elif event.event_type == EventType.QUEST_STOP:
            self.stop()
        elif event.event_type == EventType.QUEST_RELOAD:
            self.reload()
        elif event.event_type == EventType.SOUND_VOL_CHANGED:
            self.player.volume = event.event_data

        if devices.door2.is_open and \
                self.progress < Progress.PASSED_TRUNKS and \
                event.event_type == EventType.SENSOR_DATA_CHANGED and \
                event.event_device == devices.trunks and \
                event.event_data['detected'] == True:
            pin = event.event_data['pin']

            if pin == self.trunks_right[self.trunk_index]:
                self.aro += 1
                self.trunk_index += 1
                if self.trunk_index == len(self.trunks_right) - 1:
                    # Команда справилась с сундуками
                    devices.door3.is_open = True
                    self.progress = Progress.PASSED_TRUNKS
                    self.player.load("door.mp3")
            else:
                self.aro -= 1

        # if devices.door3.is_open and \
        #         self.progress < Progress.PASSED_RFID and \
        #         event.event_type == EventType.SENSOR_DATA_CHANGED and \
        #         event.event_device == devices.rfid and \
        #         event.event_data['detected'] == True:
        #     self.progress = Progress.PASSED_RFID
        #     devices.door4.is_open = True

        if devices.door4.is_open and \
                self.progress < Progress.PASSED_EQUALIZER and \
                event.event_type == EventType.SENSOR_DATA_CHANGED and \
                event.event_device == devices.equalizer and \
                event.event_data['detected'] == True:
            self.progress = Progress.PASSED_EQUALIZER
            devices.door5.is_open = True

        if devices.door5.is_open and \
                self.progress < Progress.PASSED_TREE and \
                event.event_type == EventType.SENSOR_DATA_CHANGED and \
                event.event_device == devices.tree and \
                event.event_data['detected'] == True:
            self.progress = Progress.PASSED_TREE
            devices.door6.is_open = True

        if devices.door6.is_open and \
                self.progress < Progress.PASSED_BARREL and \
                event.event_type == EventType.SENSOR_DATA_CHANGED and \
                event.event_device == devices.barrel and \
                event.event_data['detected'] == True:
            self.progress = Progress.PASSED_BARREL
            devices.door7.is_open = True

    def reload(self):
        for door in devices.doors:
            door.is_open = False

    def legend(self):
        self.start_time = time.time()
        self.in_process = True
        # self.start_timer()
        self.player.load("legend.mp3")
        Timer(38.7, devices.altars.blink_all).start()
        Timer(57, devices.board.start).start()

        def give15aro():
            self.aro += 15

        Timer(77, give15aro).start()

        def start_timer():
            self.timer = threading.Thread(target=self.handle_timer, daemon=True)
            self.timer.start()

        Timer(79, start_timer).start()

        def start_altar1():
            self.player.load("secret1.mp3")
            devices.altars.actived = 1

            def open_door1():
                time.sleep(19)
                self.player.load("door.mp3")
                devices.door1.is_open = True

            Timer(33, open_door1).start()

        Timer(87, start_altar1).start()

    def stop(self):
        self.player.stop()
        self.in_process = False
        for door in devices.doors:
            door.is_open = True

    def get_time(self):
        if self.in_process:
            return time.time() - self.start_time
        else:
            return 0

    def handle_altars(self, data):
        # _volumer = data[:-5]
        # volumer = []
        # for v in range(5):
        #     if sum(_volumer[v*4:v*4+4]) > 0:
        #         volumer.append(1)
        #     else:
        #         volumer.append(0)
        #
        # gercon = data[-5:]
        # if self.current_altar == 1:
        #     if volumer[0] == 1 and gercon[0] == 1:
        #         return "01000"
        return ""

    @property
    def fulltime_minutes(self):
        return self._fulltime_minutes

    @fulltime_minutes.setter
    def fulltime_minutes(self, new_ftime):
        if new_ftime < 0:
            new_ftime = 0
        self._fulltime_minutes = new_ftime

    @property
    def aro(self):
        return self._aro

    @aro.setter
    def aro(self, new_aro):
        if new_aro <= 50:
            self._aro = max(new_aro, 0)
        devices.board.set_runes(self.aro)
        self.observer.push_event(Event(EventType.ARO_REFRESH, self.aro))

    def handle_timer(self):
        while self.in_process:
            devices.board.set_timer(6 - self.get_time() // 900)
            time.sleep(5)
