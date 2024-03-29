import threading
import logging, logging.config
from configs.log_config import log_config
from events import Event, EventType
from player import Player, BGPlayer
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
    reloaded = False
    observer = None
    _fulltime_minutes = 90
    in_process = False
    progress = Progress.JUST_STARTED
    prev_bg_vol = 70
    _aro = 0

    def __init__(self, name, player: Player, bg_player: BGPlayer, devices):
        # threading.Thread.__init__(self)
        # self.daemon = True
        self.name = name
        self.player = player
        self.bg_player = bg_player
        self.devices = devices
        self.trunks_opened = []
        self.trunks_current = list(range(1, 7))
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
        elif event.event_type == EventType.SOUND_PLAY_START:
            self.bg_player.volume = 15
        elif event.event_type == EventType.SOUND_PLAY_STOP:
            self.bg_player.volume = self.prev_bg_vol
        elif event.event_type == EventType.MUSIC_VOL_CHANGED:
            self.bg_player.volume = event.event_data
            self.prev_bg_vol = self.bg_player.volume

        if event.event_type == EventType.SENSOR_DATA_CHANGED and self.in_process:
            if event.event_device == self.devices.trunks:
                pin = event.event_data['pin']
                if pin == 0:
                    return
                self.logger.info("OPENED TRUNK: " + str(pin))

                if pin not in self.trunks_opened:
                    self.logger.warning(self.trunks_current)
                    self.trunks_opened.append(pin)

                    if len(self.trunks_current) == 0:
                            self.aro -= 1
                            self.player.load("sunduk1aro.mp3")
                    else:
                        self.logger.warning("Trunks: pin: {}, right is {}".format(pin, self.trunks_current[0]))
                        if pin != self.trunks_current[0]:
                            self.aro -= 1
                            self.player.load("sunduk1aro.mp3")
                            self.logger.warning("Wrong Trunk, losing aros")

                    if pin in self.trunks_current:
                        self.trunks_current.remove(pin)
                        if len(self.trunks_current) == 0:
                            self.logger.info("Trunks passed successfully")
                            self.progress = Progress.PASSED_TRUNKS  # Команда справилась с сундуками

                else:
                    self.logger.warning('Trunk already opened')

            if event.event_device == self.devices.altars:
                data = event.event_data.split(":")
                self.logger.debug("Altar sent data {}".format(data))
                if data[1] == '0':
                    self.aro -= 1
                    self.player.load("minusAro.mp3")
                else:
                    self.devices.altars.turn_off_all()
                    if data[0] == '1':
                        self.aro += 2
                        self.player.load("plus2Aro.mp3")
                        time.sleep(4)
                        self.player.load("story1.mp3")
                        time.sleep(27)
                        self.player.load("secret2.mp3")
                        self.devices.altars.actived = 2
                        time.sleep(17)
                        self.devices.door2.is_open = True
                        self.player.load('door.mp3')
                    if data[0] == '2':
                        self.aro += 3
                        self.player.load("plus3Aro.mp3")
                        time.sleep(6)
                        self.player.load("story2.mp3")
                        time.sleep(33)
                        self.player.load("secret3.mp3")
                        self.devices.altars.actived = 3
                        time.sleep(19)
                        self.devices.door3.is_open = True
                        self.player.load('door.mp3')
                    if data[0] == '3':
                        self.aro += 4
                        self.player.load("plus4Aro.mp3")
                        time.sleep(6)
                        self.player.load("story3.mp3")
                        time.sleep(36)
                        self.player.load("secret4.mp3")
                        self.devices.altars.actived = 4
                        time.sleep(16)
                        self.devices.door4.is_open = True
                        self.player.load('door.mp3')
                    if data[0] == '4':
                        self.aro += 5
                        self.player.load("plus5Aro.mp3")
                        time.sleep(6)
                        self.player.load("story4.mp3")
                        time.sleep(28)
                        self.player.load("secret5.mp3")
                        self.devices.altars.actived = 5
                        time.sleep(18)
                        self.devices.door6.is_open = True
                        self.player.load('door.mp3')
                    if data[0] == '5':
                        self.aro += 6
                        self.player.load("plus6Aro.mp3")
                        time.sleep(6)
                        self.player.load("story5.mp3")

            # if self.devices.door3.is_open and \
            #         self.progress < Progress.PASSED_RFID and \
            #         event.event_type == EventType.SENSOR_DATA_CHANGED and \
            #         event.event_device == self.devices.rfid and \
            #         event.event_data['detected'] == True:
            #     self.progress = Progress.PASSED_RFID
            #     self.devices.door4.is_open = True

            if event.event_device == self.devices.door5 and \
                    event.event_data['detected'] is True:
                self.logger.info("Door with tits passed successfully")
                self.player.load("event.mp3")
                time.sleep(4)
                self.player.load("door.mp3")

            if event.event_device == self.devices.tree and \
                    event.event_data['detected'] is True:
                self.player.load("event.mp3")
                self.logger.info("Tree passed successfully")

            if event.event_device == self.devices.barrel and \
                    event.event_data['detected'] is True:
                self.player.load("event.mp3")
                time.sleep(5)
                self.devices.door7.is_open = True
                self.player.load("door.mp3")
                self.logger.info("Barrel passed successfully")

            if event.event_device in [self.devices.runes, self.devices.statues, self.devices.horns] and \
                    event.event_data['detected'] is True:
                self.logger.info("Wow, dop {} passed successfully".format(event.event_device.name))
                self.player.load("plus5Aro.mp3")
                self.aro += 5

    def reload(self):
        self.logger.info("Reloading...")
        if self.in_process:
            self.stop()
        self.in_process = False
        self.reloaded = True
        self.aro = 0
        self._fulltime_minutes = 90
        self.devices.board.set_timer(0)
        self.bg_player.load("reload.mp3")
        self.devices.altars.turn_off_all()
        Timer.cancel_timers()
        self.trunks_opened = []
        self.trunks_current = list(range(1, 7))

        for em in self.devices.ems:
            if em.can_activate:
                em.activate()
                time.sleep(0.2)

        for dop in self.devices.dops:
            dop.activate()
            time.sleep(0.2)

        time.sleep(2)
        for em in self.devices.ems:
            time.sleep(0.3)
            em.is_open = False
        self.logger.info("Quest reloaded.")

    def legend(self):
        self.logger.info("Starting...")
        self.observer.push_event(Event(EventType.QUEST_RELOADED))
        self.reloaded = False
        self.bg_player.load_dir("sounds/music")
        self.start_time = time.time()
        self.in_process = True
        for em in self.devices.ems:
            if em.can_start and em not in self.devices.dops:
                em.start()

        self.player.load("legend.mp3")
        Timer(38.7, self.devices.altars.blink_all).start()
        Timer(56, self.devices.board.start).start()

        def give15aro():
            self.aro = 15

        Timer(76.7, give15aro).start()

        def start_timer():
            self.timer = threading.Thread(target=self.handle_timer, daemon=True)
            self.timer.start()

        Timer(79.3, start_timer).start()

        def start_altar1():
            self.player.load("secret1.mp3")
            print("secret1")
            self.devices.altars.actived = 1

            def open_door1():
                self.player.load("door.mp3")
                self.devices.door1.is_open = True

            Timer(19, open_door1).start()

        Timer(86, start_altar1).start()
        self.logger.info("Quest started.")

    def stop(self):
        self.logger.info("Stopping...")
        self.observer.push_event(Event(EventType.QUEST_RELOADED))
        self.trunks_current = list(range(1, 7))
        self.devices.altars.turn_off_all()
        self.player.stop()
        self.bg_player.stop()
        self.in_process = False
        self.reloaded = False
        for em in self.devices.ems:
            em.is_open = True
            time.sleep(0.5)
        Timer.cancel_timers()
        self.logger.info("Quest stopped.")

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
        self.devices.board.set_runes(self._aro)
        self.observer.push_event(Event(EventType.ARO_REFRESH, self._aro))

    def handle_timer(self):
        while self.in_process:
            self.devices.board.set_timer(6 - int(((self.get_time() / 60) / self.fulltime_minutes)*6))

            time.sleep(5)

    def __del__(self):
        self.bg_player.stop()