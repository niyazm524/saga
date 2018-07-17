from events import Event, EventType
from pprint import pformat
from collections import deque
from concurrent.futures import ThreadPoolExecutor


class Observer:
    handlers = []
    last_id = 0
    last_10 = deque(maxlen=10)

    def __init__(self, quest, logger):
        self.quest = quest
        self.logger = logger
        self.pool = ThreadPoolExecutor(5)

    def push_event(self, event: Event):
        self.last_id += 1
        event.event_id = self.last_id
        self.last_10.appendleft(event)
        self.logger.debug("New event! "+pformat(event))
        self.pool.submit(self.quest.update, event)

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
