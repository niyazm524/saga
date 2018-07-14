from events import Event, EventType
from handler import Handler
from pprint import pformat
from collections import deque


class Observer:
    handlers = []
    last_id = 0
    last_10 = deque(maxlen=10)

    def __init__(self, logger):
        self.logger = logger

    def subscribe(self, handler: Handler):
        if handler not in self.handlers:
            self.handlers.append(handler)
            self.logger.debug("New subscription for event {}".format(handler.clause_event))

    def push_event(self, event: Event):
        self.last_id += 1
        event.event_id = self.last_id
        self.last_10.appendleft(event)
        self.logger.debug("New event! "+pformat(event))
        for handler in self.handlers:
            if handler.check_event(event):
                handler.fired_event = event
                handler()

    def poll_news(self, last_new):
        if last_new == self.last_id:
            return None
        elif self.last_id-last_new > 10:
            return []
        else:
            new_events = []
            for event in self.last_10:
                if event.event_id > last_new:
                    new_events.append(event.__dict__())
                else:
                    break
            new_events.reverse()
            return new_events