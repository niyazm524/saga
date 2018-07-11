import threading
import logging, logging.config
from log_config import log_config
import time


class Quest(threading.Thread):
    quit = False
    start_time = None

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = name
        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger("quest")
        self.logger.info("Quest {} initiated".format(self.name))

    def run(self):
        while not self.quit:
            pass
            time.sleep(5)

    def reload(self):
        pass

    def legend(self):
        self.start_time = time.time()

    def stop(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info("__exit__")
