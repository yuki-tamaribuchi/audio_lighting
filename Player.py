import numpy as np
import sounddevice
import time
from Lighting import Lighting
import vlc
from multiprocessing import Process

class Player():


    def __init__(self,file,data_instance,light_instance):
        self.color_data=data_instance.xy
        self.brightness_data=data_instance.brightness
        if data_instance.brightness_from_video:
            self.brightness_v_data=data_instance.brightness_from_video
        else:
            self.brightness_v_data=None
        self.audio_time_length=data_instance.audio_time_length
        self.p=vlc.MediaPlayer()
        self.p.set_mrl(file)
        self.processes=[
            Process(target=self.lt1.brightness,args=(self.brightness_data,self.audio_time_length,self.brightness_v_data)),
            Process(target=self.lt1.color,args=(self.color_data,self.audio_time_length)),
        ]


    def play(self):

        self.p.play()
        print('Audio Length=',round(self.audio_time_length),'sec')
        for prs in self.processes:
            prs.start()
        time.sleep(self.audio_time_length)


    def print_array(self,lighting_data):
        array_len=len(lighting_data['left'][0])
        interval=1/(array_len/self.audio_time_length)

        print(interval)

        for i in range(0,array_len,1):
            print(lighting_data['left'][0][i],',',lighting_data['right'][0][i])
            time.sleep(interval)


