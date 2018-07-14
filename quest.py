import threading
import logging, logging.config
from configs.log_config import log_config
from observer import Observer
from events import Event, EventType
import time


class Quest(threading.Thread):
    quit = False
    start_time = None
    in_process = False

    def __init__(self, name, observer: Observer):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = name
        self.observer = observer
        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger("quest")
        self.logger.info("Quest {} initiated".format(self.name))

    def run(self):
        self.observer.push_event(EventType.PROGRAM_STARTED)
        while not self.quit:
            pass
            time.sleep(5)

    def reload(self):
        self.observer.push_event(Event(EventType.QUEST_RELOAD))

    def legend(self):
        self.start_time = time.time()
        self.in_process = True
        self.observer.push_event(Event(EventType.QUEST_START))

    def stop(self):
        self.in_process = False
        self.observer.push_event(Event(EventType.QUEST_STOP))

    def get_time(self):
        if self.in_process:
            return time.time() - self.start_time
        else:
            return 0

    def __del__(self):
        self.logger.info("__del__")
