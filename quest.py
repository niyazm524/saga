import threading
import logging, logging.config
from configs.log_config import log_config
from events import Event, EventType
from player import Player
import configs.device_config as devices
import time


class Quest:
    quit = False
    start_time = None
    observer = None
    _fulltime_minutes = 90
    in_process = False
    aro = 0
    current_altar = 0

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

    def reload(self):
        for door in devices.doors:
            door.is_open = False

    def legend(self):
        self.start_time = time.time()
        self.in_process = True

        self.player.say_text("some start file")
        time.sleep(3)
        devices.altar1.blink_all()
        time.sleep(3)
        devices.board.start()
        time.sleep(3)
        self.player.load("secret1.mp3")
        devices.altar1.turn_on()
        self.current_altar = 1
        time.sleep(19)
        self.player.load("door.mp3")
        devices.door1.is_open = True

    def stop(self):
        self.in_process = False

    def get_time(self):
        if self.in_process:
            return time.time() - self.start_time
        else:
            return 0

    def handle_altars(self, data):
        _volumer = data[:-5]
        volumer = []
        for v in range(5):
            if sum(_volumer[v*4:v*4+4]) > 0:
                volumer.append(1)
            else:
                volumer.append(0)

        gercon = data[-5:]
        if self.current_altar == 1:
            if volumer[0] == 1 and gercon[0] == 1:
                return "01000"

    @property
    def fulltime_minutes(self):
        return self._fulltime_minutes

    @fulltime_minutes.setter
    def fulltime_minutes(self, new_ftime):
        if new_ftime < 0:
            new_ftime = 0
        self._fulltime_minutes = new_ftime