import threading
import time


class Quest(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.board = 1

    def run(self):
        while True:
            self.board += 1
            print(self.board)
            time.sleep(5)
