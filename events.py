import time
from enum import Enum
from devices import DeviceType


class EventType(Enum):
    SENSOR_DATA_CHANGED = 1
    WEB_BUTTON_CLICKED = 2
    QUEST_START = 3
    QUEST_STOP = 4
    QUEST_RELOAD = 5
    SOUND_PLAY_START = 6
    DOOR_OPENED = 7
    DOOR_LOCKED = 8
    PROGRAM_STARTED = 9


class Event():
    event_id = None
    event_type = None
    event_time = time.time()
    event_device = None
    event_data = None

    def __init__(self, event_type, event_data=None, event_device=None):
        self.event_type = event_type
        self.event_data = event_data
        self.event_device = event_device

    def __dict__(self):
        return {"event_id": self.event_id, "event_type": self.event_type.value, "event_data": self.event_data}

    def __eq__(self, other):
        return self.event_type == other.event_type and self.event_data == other.event_data

    def __format__(self, format_spec):
        return "<Event> {} with data {}".format(self.event_type.name, self.event_data)

    def __repr__(self):
        return "<Event> {} with data {}".format(self.event_type.name, self.event_data)

    def __str__(self):
        return "<Event> {} with data {}".format(self.event_type.name, self.event_data)
