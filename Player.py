import time
from Lighting import Lighting
import vlc
from multiprocessing import Process

class Player():


    def __init__(self,file,data_instance,light_instance):
        self.__color_data=data_instance.xy
        self.__brightness_data=data_instance.brightness
        if data_instance.brightness_from_video:
            self.__brightness_v_data=data_instance.brightness_from_video
        else:
            self.__brightness_v_data=None
        self.__audio_time_length=data_instance.audio_time_length

        self.__p=vlc.MediaPlayer()
        self.__p.set_mrl(file)
        self.__processes=[
            Process(target=light_instance.brightness,args=(self.__brightness_data,self.__audio_time_length,self.__brightness_v_data)),
            Process(target=light_instance.color,args=(self.__color_data,self.__audio_time_length)),
        ]


    def play(self):

        self.__p.play()
        print('Audio Length=',round(self.__audio_time_length),'sec')
        for prs in self.__processes:
            prs.start()
        time.sleep(self.__audio_time_length)
