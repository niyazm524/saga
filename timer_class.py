from threading import Timer

timers = list()


class TimerClass(Timer):
    def __init__(self, interval, func, *args, **kwargs):
        super().__init__(interval, func, args, kwargs)

        timers.append(self)

    def __del__(self):
        timers.remove(self)


def cancel_timers():
    for tim in timers:
        try:
            tim.cancel()
        except:
            pass
    timers = []