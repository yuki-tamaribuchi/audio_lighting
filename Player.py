import numpy as np
import sounddevice
import time
from Lighting import Lighting
import vlc
import asyncio

class Player():


    def __init__(self,file,audio_time_length,color_data=None,brightness_data=None):
        self.lt1=Lighting('192.168.11.99')
        self.color_data=color_data
        self.brightness_data=brightness_data
        self.audio_time_length=audio_time_length
        self.p=vlc.MediaPlayer()
        self.p.set_mrl(file)


    def play_w_lightring(self):

        self.p.play()
        print('Audio Length=',round(self.audio_time_length),'sec')
        asyncio.run(self.lighting())
        time.sleep(self.audio_time_length)


    async def lighting(self):
        task_brightness=asyncio.create_task(
            self.lt1.brightness(data=self.brightness_data,audio_time_length=self.audio_time_length)
        )
        task_color=asyncio.create_task(
            self.lt1.color(data=self.color_data,audio_len=self.audio_time_length)
        )
        await task_brightness
        await task_color


    def print_array(self,lighting_data):
        array_len=len(lighting_data['left'][0])
        interval=1/(array_len/self.audio_time_length)

        print(interval)

        for i in range(0,array_len,1):
            print(lighting_data['left'][0][i],',',lighting_data['right'][0][i])
            time.sleep(interval)


