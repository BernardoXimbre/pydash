import time

from player.parser import *
from r2a.ir2a import IR2A

class r2a_grupo10(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.qi = []
        self.throughputs = int(0xFFFFFFF)
        self.cwnd = 0
        self.mss = 0
        self.request_time = 0
        self.selected_qi = 0
    
        pass
   
    def handle_xml_request(self, msg): 
        self.request_time = time.perf_counter()
        self.send_down(msg)

    def handle_xml_response(self, msg):
        parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = parsed_mpd.get_qi()
        self.mss = self.qi[0]
        self.cwnd = self.mss*4

        self.send_up(msg)
   
    def handle_segment_size_request(self, msg):
        self.request_time = time.perf_counter()

        print('>>>>>CWND>>>>>')
        print(self.cwnd)
        print('>>>>>MSS>>>>>')
        print(self.mss)

        if self.cwnd > self.throughputs:
            self.selected_qi = 0
            self.mss = self.qi[0]*2
            self.cwnd = self.mss

        else:
            while self.qi[self.selected_qi] < self.cwnd:
                self.selected_qi+= 1
            self.mss += self.mss
            self.cwnd = (self.mss*self.mss)/self.cwnd

        print('>>>>>qi>>>>>')
        print(self.qi[self.selected_qi-1])

        
        msg.add_quality_id(self.qi[self.selected_qi-1])
        
        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        t = time.perf_counter() - self.request_time
        self.throughputs = msg.get_bit_length()/t

        print('>>>>>>throughputs>>>>>>')
        print(self.throughputs)
        
        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass
