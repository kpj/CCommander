from __future__ import division

import numpy as np
import pickle
import os, os.path
import struct
import sys
import time
import wave

import pyaudio

import ccommander.utils
import ccommander.commander


class MusicFileParser(object):
    def __init__(self, path):
        self.path = self.ensure_wav(path.encode('UTF-8').decode('UTF-8'))

    def ensure_wav(self, path):
        """Checks if path directs to a wav file and creates one if not
        """
        if path[-3:] != 'wav':
            output = '/tmp/%s.wav' % os.path.basename(path)[:-4]

            print('Converting "%s" to "%s"' % (path, output))
            os.system('ffmpeg -loglevel error -y -i "%s" "%s"' % (path, output))

            return output
        return path

class MusicPlayer(object):
    def __init__(self, path):
        self.parser = MusicFileParser(path)
        self.commander = ccommander.commander.Commander()

        self.player = pyaudio.PyAudio()

        self.file = wave.open(self.parser.path, 'rb')
        self.stream = self.player.open(
            format=self.player.get_format_from_width(self.file.getsampwidth()),
            channels=self.file.getnchannels(),
            rate=self.file.getframerate(),
            output=True,
            stream_callback=self.callback
        )

        self.prev = 0
        self.avg_diffs = ccommander.utils.ConstantLengthList(20)

    def handle(self, data, frame_count):
        data = np.array(struct.unpack_from ("%dh" % frame_count, data))

        fft_data = abs(np.fft.rfft(data))**2
        maxi = fft_data[1:].argmax() + 1
        quot = self.file.getframerate()/frame_count

        if maxi != len(fft_data)-1:
            y0, y1, y2 = np.log(fft_data[maxi-1:maxi+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)

            freq = (maxi+x1)*quot
        else:
            freq = maxi*quot

        diff = freq - self.prev
        self.avg_diffs.append(abs(diff))

        #print(freq, freq - self.prev, self.avg_diffs.get_avg())
        if diff > self.avg_diffs.get_avg():
            self.commander.new_random_color()

        self.prev = freq

    def callback(self, in_data, frame_count, time_info, status):
        data = self.file.readframes(frame_count)
        self.handle(data, frame_count)

        return (data, pyaudio.paContinue)

    def play(self):
        self.stream.start_stream()

        while self.stream.is_active():
            time.sleep(0.1)

        self.stream.stop_stream()
        self.stream.close()
        self.player.terminate()

def main(path):
    mp = MusicPlayer(path)
    mp.play()


if __name__ == '__main__':
    main(sys.argv[1])
