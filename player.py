from subprocess import Popen, PIPE, STDOUT, DEVNULL


class Player:
    paused = None
    current_sound_file = None

    def __init__(self, volume=60):
        self.proc = Popen(["mpg321", "-R", "word"], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        self._volume = volume
        self.volume = volume
        self.proc.stdin.write('LOAD test.mp3\n')

    def rc(self, command: str):
        self.proc.stdin.write(str.encode(command+'\n'))

    def load(self, sound_file):
        self.rc("LOAD " + sound_file)
        self.current_sound_file = sound_file
        self.paused = False

    def pause(self):
        self.rc("PAUSE")
        self.paused = not self.paused

    def stop(self):
        self.rc("STOP")
        self.paused = None

    def quit(self):
        self.rc("QUIT")

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, new_volume):
        self.rc("GAIN "+str(new_volume))
        self._volume = new_volume

p = Player()