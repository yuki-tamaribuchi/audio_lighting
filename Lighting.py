from phue import Bridge
import time

class Lighting():

    def __init__(self,ip_addr):
        b=Bridge(ip_addr)
        b.connect()
        self.lights=b.lights
        self.lights[0].brightness=127

    def brightness(self,data,audio_len):
        data_length=len(data)
        print(data_length)
        interval=audio_len/data_length
        print(interval)
        for i in range(0,data_length):
            self.lights[0].brightness=127+(int(data[i])*30)
            print(data[i])
            time.sleep(interval)