from events import Event, EventType
from handler import Handler


class Observer:
    handlers = []

    def __init__(self, logger):
        self.logger = logger

    def subscribe(self, handler: Handler):
        if handler not in self.handlers:
            self.handlers.append(handler)
