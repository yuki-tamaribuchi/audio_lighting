import numpy as np
import sounddevice
import time

class Player():

    def __init__(self,audio_data,rate,lighting_data=None):
        self.audio_data=audio_data
        self.rate=rate
        self.lighting_data=lighting_data


    def play_w_lightring(self):
        sounddevice.play(self.audio_data,self.rate)
        audio_len=len(self.audio_data)/self.rate
        print('Audio Length=',round(audio_len),'sec')
        time.sleep(audio_len)

