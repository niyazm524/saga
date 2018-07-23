from subprocess import Popen, PIPE, STDOUT, DEVNULL
import threading
from events import Event, EventType
import os, signal, time


class BGPlayer:
    paused = None
    observer = None
    vol_down = None
    proc = None

    def __init__(self, volume=60):
        self._volume = volume
        self.prev_volume = volume

    def load(self, sound_file):
        if self.proc is not None:
            self.proc.terminate()
        self.proc = Popen(["mpg321", "--loop", "0", "-K", "--gain", str(self.volume), "sounds/"+sound_file], stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL)
        try:
            self.observer.push_event(Event(EventType.MUSIC_PLAY_START, sound_file))
        except:
            pass
        self.paused = False

    def load_dir(self, directory):
        if self.proc is not None:
            self.proc.kill()
        self.proc = Popen(["mpg321", "--loop", "0", "-B", "-K", "--gain", str(self.volume), directory], stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL)
        try:
            self.observer.push_event(Event(EventType.MUSIC_PLAY_START_PLAY_START))
        except:
            pass
        self.paused = False

    def stop(self):
        if self.proc is not None:
            self.proc.kill()

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, new_volume):
        self.volume_shift((new_volume - self._volume) // 3)

    def volume_shift(self, vol):
        if self.proc is None:
            return
        if vol > 0:
            sym = b"*"
        elif vol < 0:
            sym = b"/"
        else:
            return

        self._volume = self._volume + vol*3
        if vol > 0:
            for _ in range(abs(vol)):
                self.proc.stdin.write(sym)
                self.proc.stdin.flush()
                time.sleep(0.08)
        else:
            self.proc.stdin.write(sym * abs(vol))
            self.proc.stdin.flush()

    def mute(self):
        if self.proc is None:
            return
        self.proc.stdin.write(b"m")
        self.proc.stdin.flush()


class Player:
    paused = None
    current_sound_file = None
    observer = None

    def __init__(self, volume=60):
        self.proc = Popen(["mpg321", "-R", "word"], stdin=PIPE, stdout=PIPE, stderr=DEVNULL)
        self._volume = volume
        self.volume = volume
        self.prev_volume = volume
        self.thread = threading.Thread(target=self.std_read, args=(), daemon=True)
        self.thread.start()

    def rc(self, command: str):
        self.proc.stdin.write((command+'\n').encode('UTF-8'))
        self.proc.stdin.flush()

    def load(self, sound_file):
        try:
            self.observer.push_event(Event(EventType.SOUND_PLAY_START, sound_file))
        except:
            pass
        time.sleep(0.1)
        self.rc("LOAD " + "sounds/"+sound_file)
        self.current_sound_file = sound_file

        self.paused = False

    def std_read(self):
        while True:
            line = self.proc.stdout.readline()
            if line != '':
                if line[:2] == b"@P":
                    self.observer.push_event(Event(EventType.SOUND_PLAY_STOP))
            else:
                break

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
        os.system('echo "{}" | festival --tts'.format(text))
        # Popen('/bin/echo "{}" | festival -tts'.format(text), close_fds=True)
        # os.spawnl(os.P_NOWAIT, 'echo "{}" | festival -tts'.format(text), "")

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, new_volume):
        self.rc("GAIN "+str(new_volume))
        self.prev_volume = self._volume
        self._volume = new_volume