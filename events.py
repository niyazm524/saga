import time
from enum import Enum


class EventType(Enum):
    SENSOR_DATA_CHANGED = 1
    WEB_BUTTON_CLICKED = 2
    QUEST_STARTED = 3
    QUEST_STOPPED = 4
    QUEST_RELOADED = 5
    SOUND_PLAY_START = 6
    DOOR_OPENED = 7
    DOOR_LOCKED = 8


class Event:
    event_type = None
    event_time = time.time()
    event_data = None

    def __init__(self, event_type, event_data):
        self.event_type = event_type
        self.event_data = event_data

    def __eq__(self, other):
        return self.event_type == other.event_type and self.event_data == other.event_data
