from events import Event, EventType


class Handler:
    BY_TYPE = 1
    BY_TYPE_AND_DATA = 2

    def __init__(self, clause: Event, action_func, conformity_by=BY_TYPE_AND_DATA):
        self.clause_event = clause
        self.action_func = action_func
        self.conformity_by = conformity_by
        self.fired_event = None

    def check_event(self, event: Event):
        if self.conformity_by == Handler.BY_TYPE_AND_DATA:
            return event == self.clause_event
        elif self.conformity_by == Handler.BY_TYPE:
            return event.event_type == self.clause_event.event_type

    def __call__(self, *args, **kwargs):
        self.action_func(*args, **kwargs)
