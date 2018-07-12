from events import Event, EventType
from handler import Handler
from pprint import pformat


class Observer:
    handlers = []

    def __init__(self, logger):
        self.logger = logger

    def subscribe(self, handler: Handler):
        if handler not in self.handlers:
            self.handlers.append(handler)
            self.logger.debug(
                f"New subscription for event type {handler.clause_event.event_type.name} "
                f"and event data {handler.clause_event.event_data}")

    def push_event(self, event: Event):
        self.logger.debug("New event! "+pformat(event))
        for handler in self.handlers:
            if handler.check_event(event):
                handler.fired_event = event
                handler()
