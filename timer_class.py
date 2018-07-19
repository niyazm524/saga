from threading import Timer


class TimerClass(Timer):
    timers = list()

    def __init__(self, interval, func, *args, **kwargs):
        super().__init__(interval, func, args, kwargs)

        TimerClass.timers.append(self)

    def __del__(self):
        TimerClass.timers.remove(self)

    @staticmethod
    def cancel_timers():
        for tim in TimerClass.timers:
            try:
                tim.cancel()
            except:
                pass
        TimerClass.timers = []
