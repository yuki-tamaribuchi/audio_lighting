import numpy as np
import sounddevice

class Player():

    def __init__(self,audio_data,rate,lighting_data=None):
        self.audio_data=audio_data
        self.rate=rate
        self.lighting_data=lighting_data


    def play_w_lightring(self):
        sounddevice.play(data=self.audio_data,rate=self.rate)