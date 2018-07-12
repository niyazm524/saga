import threading
import logging, logging.config
from log_config import log_config
from observer import Observer
from events import Event, EventType
import time


class Quest(threading.Thread):
    quit = False
    start_time = None

    def __init__(self, name, observer: Observer):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = name
        self.observer = observer
        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger("quest")
        self.logger.info("Quest {} initiated".format(self.name))

    def run(self):
        while not self.quit:
            pass
            time.sleep(5)

    def reload(self):
        self.observer.push_event(Event(EventType.QUEST_RELOAD))

    def legend(self):
        self.start_time = time.time()
        self.observer.push_event(Event(EventType.QUEST_START))

    def stop(self):
        self.observer.push_event(Event(EventType.QUEST_STOP))

    def __del__(self):
        self.logger.info("__del__")
