import time

from player.parser import *
from r2a.ir2a import IR2A

class R2AAbr(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.parsed_mpd = ''
        self.qi = []
