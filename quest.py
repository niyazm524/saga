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
    in_process = False
    aro = 0

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

    def reload(self):
        pass

    def legend(self):
        self.start_time = time.time()
        self.in_process = True

        self.player.say_text("3 grooz")
        devices.altar1.blink_all()
        devices.board.set_all(2, 1)
        self.player.say_text("zagadka 1")
        devices.altar1.turn_on()
        devices.door1.is_open = True

    def stop(self):
        self.in_process = False

    def get_time(self):
        if self.in_process:
            return time.time() - self.start_time
        else:
            return 0
