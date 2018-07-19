from events import Event, EventType
from pprint import pformat
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from devices import Device


class Observer:
    handlers = []
    last_id = 0
    last_10 = deque(maxlen=10)
    ignored_list = [EventType.SOUND_PLAY_START, EventType.ALTARS_WEB_REFRESH]

    def __init__(self, quest, logger, device_cfg, player):
        self.quest = quest
        self.quest.observer = self
        self.logger = logger
        self.player = player
        self.player.observer = self
        self.device_cfg = device_cfg
        self.devices = [getattr(device_cfg, device) for device in dir(device_cfg)
                        if isinstance(getattr(device_cfg, device), Device)]
        self.dev_names = [device for device in dir(device_cfg) if isinstance(getattr(device_cfg, device), Device)]
        self.pool = ThreadPoolExecutor(15)

    def push_event(self, event: Event):
        self.last_id += 1
        event.event_id = self.last_id
        self.last_10.appendleft(event)
        self.logger.debug("New event! "+pformat(event))
        if event.event_type not in self.ignored_list:
            self.pool.submit(self.quest.update, event)

    def button_clicked(self, btn_id, btn_data):
        if btn_id == "time-reduce":
            self.quest.fulltime_minutes -= 5
            self.push_event(Event(EventType.FTIME_SYNC, self.quest.fulltime_minutes))
        elif btn_id == "time-add":
            self.quest.fulltime_minutes += 5
            self.push_event(Event(EventType.FTIME_SYNC, self.quest.fulltime_minutes))
        elif btn_id == "reload":
            self.push_event(Event(EventType.QUEST_RELOAD))
        elif btn_id == "start":
            self.push_event(Event(EventType.QUEST_START))
        elif btn_id == "stop":
            self.push_event(Event(EventType.QUEST_STOP))
        elif btn_id == "volume":
            self.push_event(Event(EventType.SOUND_VOL_CHANGED, event_data=btn_data))
        elif btn_id == "altars":
            a = int(btn_data)
            if 0 <= a <= 6:
                self.device_cfg.altars.actived = a
        elif btn_id == "aro-reduce":
            self.quest.aro -= 1
        elif btn_id == "aro-add":
            self.quest.aro += 1

    def door_clicked(self, door, action):
        try:
            d = getattr(self.device_cfg, door)
            if action == "open":
                d.is_open = True
            elif action == "close":
                d.is_open = False
            elif action == "act":
                d.activate()
            elif action == "deact":
                d.deactivate()
        except Exception as e:
            self.logger.error(e)

    def hint_clicked(self, hint_id):
        try:
            self.player.load("hints/hint{}.mp3".format(hint_id))
        except Exception as e:
            self.logger.error(e)

    def actlink_clicked(self, id):
        if id == "minus2aro":
            self.quest.aro -= 2
            self.player.load("tumba2aro.mp3")

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
