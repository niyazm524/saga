import threading
import logging, logging.config
from configs.log_config import log_config
from events import Event, EventType
from player import Player
import configs.device_config as devices
import time
from enum import Enum
from timer_class import TimerClass as Timer


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

        if event.event_type == EventType.SENSOR_DATA_CHANGED:
            print(event)
            if devices.door2.is_open and \
                    event.event_device == devices.trunks:
                pin = event.event_data['pin']
                print(pin)

                if pin == 1:
                    return

                if pin == self.trunks_right[self.trunk_index]:
                    self.trunk_index += 1
                    if self.trunk_index == len(self.trunks_right):
                        # Команда справилась с сундуками
                        self.progress = Progress.PASSED_TRUNKS
                else:
                    self.aro -= 1
                    self.player.load("sunduk1aro.mp3")

            if event.event_device == devices.altars:
                data = event.event_data.split(":")
                print(data)
                if data[1] == '0':
                    self.aro -= 1
                    self.player.load("minusAro.mp3")
                else:
                    if data[0] == '1':
                        self.aro += 2
                        self.player.load("plus2Aro.mp3")
                        time.sleep(4)
                        self.player.load("story1.mp3")
                        time.sleep(27)
                        self.player.load("secret2.mp3")
                        devices.altars.actived = 2
                        time.sleep(17)
                        devices.door2.is_open = True
                        self.player.load('door.mp3')
                    if data[0] == '2':
                        self.aro += 3
                        self.player.load("plus3Aro.mp3")
                        time.sleep(6)
                        self.player.load("story2.mp3")
                        time.sleep(33)
                        self.player.load("secret3.mp3")
                        devices.altars.actived = 3
                        time.sleep(19)
                        devices.door3.is_open = True
                        self.player.load('door.mp3')
                    if data[0] == '3':
                        self.aro += 4
                        self.player.load("plus4Aro.mp3")
                        time.sleep(6)
                        self.player.load("story3.mp3")
                        time.sleep(36)
                        self.player.load("secret4.mp3")
                        devices.altars.actived = 4
                        time.sleep(16)
                        devices.door4.is_open = True
                        self.player.load('door.mp3')
                    if data[0] == '4':
                        self.aro += 5
                        self.player.load("plus5Aro.mp3")
                        time.sleep(6)
                        self.player.load("story4.mp3")
                        time.sleep(28)
                        self.player.load("secret5.mp3")
                        devices.altars.actived = 5
                        time.sleep(18)
                        devices.door6.is_open = True
                        self.player.load('door.mp3')
                    if data[0] == '5':
                        self.aro += 6
                        self.player.load("plus6Aro.mp3")
                        time.sleep(6)
                        self.player.load("story5.mp3")
                        time.sleep(19)
                        devices.altars.turn_off_all()

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
            if door.can_activate:
                door.activate()
        time.sleep(5)

        for door in devices.doors:
            time.sleep(0.5)
            door.is_open = False
        devices.altars.turn_off_all()
        Timer.cancel_timers()
        self.aro = 0

    def legend(self):
        self.start_time = time.time()
        self.in_process = True
        # self.start_timer()
        self.player.load("legend.mp3")
        Timer(38.7, devices.altars.blink_all).start()
        Timer(57, devices.board.start).start()

        def give15aro():
            self.aro = 15

        Timer(77, give15aro).start()

        def start_timer():
            self.timer = threading.Thread(target=self.handle_timer, daemon=True)
            self.timer.start()

        Timer(79, start_timer).start()

        def start_altar1():
            self.player.load("secret1.mp3")
            devices.altars.actived = 1

            def open_door1():
                self.player.load("door.mp3")
                devices.door1.is_open = True

            Timer(19, open_door1).start()

        Timer(86, start_altar1).start()

    def stop(self):
        devices.altars.turn_off_all()
        self.player.stop()
        self.in_process = False
        for door in devices.doors:
            door.is_open = True
            time.sleep(0.5)
        Timer.cancel_timers()

    def get_time(self):
        if self.in_process:
            return time.time() - self.start_time
        else:
            return 0

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
        self._aro = new_aro
        if self._aro < 0: self._aro = 0
        if self._aro > 50: self._aro = 50
        devices.board.set_runes(self._aro)
        self.observer.push_event(Event(EventType.ARO_REFRESH, self._aro))

    def handle_timer(self):
        while self.in_process:
            devices.board.set_timer(6 - self.get_time() // 900)
            time.sleep(5)
