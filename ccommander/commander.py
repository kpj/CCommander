import os
import random
import serial


class Commander(object):
    """https://code.google.com/p/cirrus7-light-commander/wiki/SeriellesProtokoll
    """
    def __init__(self, path='/dev/ttyUSB0'):
        self.conn = serial.Serial(path, 9600, timeout=None)
        self.init(path)

        self.colors = ['r', 'g', 'b', 'y', 'p', 'c', 'w'] # 'o' -> off
        self.set_all_colors('o')

        self.last_color = 'o'

    def init(self, device):
        os.system('stty -F %s 9600 raw -hupcl min 0' % device)

    def send(self, data):
        """Sends data, waits for its execution to finish
           and returns something #the received data.
        """
        #print('Sending "%s"' % data)
        ret = self.conn.write(bytes('%s\r' % data, encoding='ascii'))
        return ret

    def set_all_colors(self, col):
        """Takes string or integer
        """
        if isinstance(col, str):
            self.send('s DA %s' % col)
        else:
            self.send('s da %i' % col)

        self.send('t i')

    def new_random_color(self):
        c = random.choice(self.colors)
        while c == self.last_color:
            c = random.choice(self.colors)

        self.set_all_colors(c)
        self.last_color = c
