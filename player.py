from subprocess import Popen, PIPE, STDOUT, DEVNULL
import os


class Player:
    paused = None
    current_sound_file = None

    def __init__(self, volume=60):
        self.proc = Popen(["mpg321", "-R", "word"], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        self._volume = volume
        self.volume = volume

    def rc(self, command: str):
        self.proc.stdin.write((command+'\n').encode('UTF-8'))
        self.proc.stdin.flush()

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

    @staticmethod
    def say_text(text: str):
        os.spawnl(os.P_NOWAIT, 'echo "{}" | festival -tts'.format(text))

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, new_volume):
        self.rc("GAIN "+str(new_volume))
        self._volume = new_volume
