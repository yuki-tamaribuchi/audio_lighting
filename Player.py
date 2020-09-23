import numpy as np
import sounddevice
import time
from Lighting import Lighting

class Player():


    def __init__(self,audio_data,rate,lighting_data=None):
        self.audio_data=audio_data
        self.rate=rate
        self.lighting_data=lighting_data
        self.lt1=Lighting('192.168.11.99')


    def play_w_lightring(self,brightness_data,color_data):
        sounddevice.play(self.audio_data,self.rate)
        self.audio_len=len(self.audio_data)/self.rate
        print('Audio Length=',round(self.audio_len),'sec')
        self.lt1.brightness(brightness_data,self.audio_len)
        self.lt1.color(color_data,self.audio_len)
        time.sleep(self.audio_len)


    def print_array(self,lighting_data):
        array_len=len(lighting_data['left'][0])
        print(array_len)
        interval=1/(array_len/self.audio_len)

        print(interval)

        for i in range(0,array_len,1):
            print(lighting_data['left'][0][i],',',lighting_data['right'][0][i])
            time.sleep(interval)


