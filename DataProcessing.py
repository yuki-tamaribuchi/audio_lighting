import numpy as np
import librosa
import librosa.display
from matplotlib import pyplot as plt
from scipy.io import wavfile
from scipy.signal import resample
import csv
from moviepy.video.io.VideoFileClip import VideoFileClip
import json
import os
from cv2 import cv2
from PIL import Image
from concurrent import futures
import time

import sys
np.set_printoptions(threshold=sys.maxsize)

class DataProcessing():


    def __init__(self,file,mode,concurrent_mode):
        self.brightness=[[],[]]
        self.brightness_from_video=[]
        self.concurrent_mode=concurrent_mode

        if mode=='a':
            self.__load_audio(file)
            if self.__check_temp():
                self.__load_color_data_from_csv()
                self.__load_brightness_data_from_csv()
            else:
                self.__dump_audio_array_length()
                self.__hpss_execute()
                self.__chromacens_execute()
                self.__create_brightness_data()
                self.__save_brightness_data()
                self.__create_color_data()
                self.__save_color_data()
        elif mode=='v':
            self.__load_audio_from_video(file)
            if self.__check_temp():
                self.__load_color_data_from_csv()
                self.__load_brightness_data_from_csv()
                #self.__load_brightness_data_from_video_from_csv()
            else:
                    
                #self.__dump_audio_array_length()
                self.__hpss_execute()
                self.__chromacens_execute()
                self.__create_brightness_data()
                self.__save_brightness_data()
                self.__create_color_data()
                self.__save_color_data()
                #self.__calc_brightness_from_video(file)
                #self.__save_brightness_from_video_data()
                
        else:
            print('モードを"a"，または"v"で指定してください')


    def __load_audio(self,file):
        print('Loading Start')
        self.rate,self.loaded_data=wavfile.read(file)
        self.normalized_data=self.loaded_data/32768
        #self.dump_audio_array_length()
        self.audio_time_length=len(self.normalized_data)/self.rate
        print('Loading End')


    def __load_audio_from_video(self,file):
        print('Loading Start')
        video_data=VideoFileClip(file)
        audio_data=video_data.audio
        self.normalized_data=audio_data.to_soundarray()
        self.rate=44100
        #self.dump_audio_array_length()
        self.audio_time_length=len(self.normalized_data)/self.rate
        print('Loading End')


    def __hpss_execute(self):
        print('HPSS Start')
        if self.concurrent_mode:
            results=[]
            def future_execute(self):
                with futures.ThreadPoolExecutor(max_workers=2) as executer:
                    results.append(executer.submit(librosa.effects.hpss,self.normalized_data[:,0]))
                    results.append(executer.submit(librosa.effects.hpss,self.normalized_data[:,1]))
            future_execute(self)
            self.hpss_harmonics_left,self.hpss_percussion_left=results[0].result()
            self.hpss_harmonics_right,self.hpss_percussion_right=results[1].result()
        else:
            self.hpss_harmonics_left,self.hpss_percussion_left=librosa.effects.hpss(self.normalized_data[:,0])
            self.hpss_harmonics_right,self.hpss_percussion_right=librosa.effects.hpss(self.normalized_data[:,1])
        print('HPSS End')
        

    def __chromacens_execute(self,n_bins=48,hop_length=4096,fmin=130.813,win_len_smooth=20):
        print('Chroma Cens Start')
        C_left=librosa.cqt(self.hpss_harmonics_left,n_bins=n_bins,hop_length=hop_length)
        C_right=librosa.cqt(self.hpss_harmonics_right,n_bins=n_bins,hop_length=hop_length)
        self.cens_left=librosa.feature.chroma_cens(C=C_left,hop_length=hop_length,fmin=fmin,win_len_smooth=win_len_smooth)
        self.cens_right=librosa.feature.chroma_cens(C=C_right,hop_length=hop_length,fmin=fmin,win_len_smooth=win_len_smooth)
        print('Chroma Cens End')
    

    def __dump_audio_array_length(self):
        d={'length':len(self.normalized_data)}
        with open('temp_data/temp.json','w') as f:
            json.dump(d,f)

    def __check_temp(self):
        if not os.path.isfile('temp_data/temp.json'):
            return False
        with open('temp_data/temp.json','r') as f:
            temp_data=json.load(f)
            print(temp_data['length']==len(self.normalized_data))
            return temp_data['length']==len(self.normalized_data)
                


    def __export_csv(self):
        print('Export Start')
        with open('temp_data/data.csv','w') as f:
            writer=csv.writer(f)
            writer.writerows(self.cens_left)
        print('Export End')

    def __save_color_data(self):
        print('Save Color Data Start')
        with open('temp_data/color.csv','w') as f:
            writer=csv.writer(f)
            writer.writerows(self.xy)
        print('Save Color Data End')


    def __save_brightness_data(self):
        print('Save Brightness Data Start')
        with open('temp_data/brightness.csv','w') as f:
            writer=csv.writer(f)
            writer.writerows(self.brightness)
        print('Save Brightness Data End')


    def __save_brightness_from_video_data(self):
        print('Save Brightness from Video Data Start')
        with open('temp_data/brightness_from_video.csv','w') as f:
            writer=csv.writer(f)
            writer.writerow(self.brightness_from_video)
        print('Save Brightness from Video Data Start')

    
    def __create_brightness_data(self):
        print('Create Brightness data Start')
        resample_size=int((self.audio_time_length/60)*600)
        print('Resample Size=',resample_size)
        print('S/L=',self.audio_time_length/resample_size)
        left_percussion_rs=resample(abs(self.hpss_percussion_left),resample_size)
        right_percussion_rs=resample(abs(self.hpss_percussion_right),resample_size)
        left_max=left_percussion_rs.max()
        right_max=right_percussion_rs.max()
        #0=left,1=right
        self.brightness[0]=left_percussion_rs/left_max
        self.brightness[1]=right_percussion_rs/right_max
        print('Create Brightness data End')


    def __calc_brightness_from_video(self,file):
        print('Calc Brightness from Video Start')
        vidcap=cv2.VideoCapture(file)
        is_in_loop=True
        i=0
        while is_in_loop:
            vidcap.set(cv2.CAP_PROP_POS_MSEC,i*100)
            has_frame,frame_image=vidcap.read()
            if has_frame:
                height,width=frame_image.shape[:2]
                image=Image.frombuffer(mode='RGB',size=(height,width),data=frame_image)
                greyscale_image=image.convert('L')
                histogram=greyscale_image.histogram()
                pixels=sum(histogram)
                brightness=scale=len(histogram)

                for index in range(0, scale):
                    ratio = histogram[index] / pixels
                    brightness += ratio * (-scale + index)
                self.brightness_from_video.append(1 if brightness == 255 else brightness / scale)
                i+=1
            else:
                is_in_loop=False
        print('Calc Brightness from Video End')




    def __create_color_data(self):
        print('Create Color Data Start')

        chroma_rgb=np.array([
            #Kari Ziets' research 1931
            #Color Name to RGB Reference -> https://web.njit.edu/~walsh/rgb.html

            #C,ド,Red
            [255,0,0],

            #C#,ド#(レb),Purple
            [160,32,240],

            #D,レ,Violet
            [238,130,238],

            #D#,レ#(ミb),LightBlue
            [173,216,230],

            #E,ミ,Gold
            [255,215,0],

            #F,ファ,Pink
            [255,192,203],

            #F#,ファ#(ソb),turquoise4
            [0,134,139],

            #G,ソ,SkyBlue
            [135,206,235],

            #G#,ソ#(ラb),Unknown -> mean of G and A
            [195,230,79],

            #A,ラ,冷たい黄 -> Yellow
            [255,255,0],

            #A#,ラ#(シb),Orange
            [255,165,0],

            #B,シ,Copper
            [184,115,51]
        ])

        left_rgb=chroma_rgb[self.cens_left.real.argmax(axis=0)]
        right_rgb=chroma_rgb[self.cens_right.real.argmax(axis=0)]
        left_xy=np.nan_to_num(np.apply_along_axis(self.__convert_rgb_to_xy,1,left_rgb))
        right_xy=np.nan_to_num(np.apply_along_axis(self.__convert_rgb_to_xy,1,right_rgb))
        self.xy=np.hstack([left_xy,right_xy])
        print('Create Color Data End')
        

    def __convert_rgb_to_xy(self,data):
        r_gamma = pow( ((data[0]/256) + 0.055) / (1.0 + 0.055), 2.4 ) if (data[0]/256) > 0.04045 else ((data[0]/256) / 12.92)
        g_gamma = pow( ((data[1]/256) + 0.055) / (1.0 + 0.055), 2.4 ) if (data[1]/256) > 0.04045 else ((data[1]/256) / 12.92)
        b_gamma = pow( ((data[2]/256) + 0.055) / (1.0 + 0.055), 2.4 ) if (data[2]/256) > 0.04045 else ((data[2]/256) / 12.92)

        x = r_gamma * 0.649926 + g_gamma * 0.103455 + b_gamma * 0.197109
        y = r_gamma * 0.234327 + g_gamma * 0.743075 + b_gamma * 0.022598
        z = g_gamma * 0.053077 + b_gamma * 1.035763

        x=x/(x+y+z)
        y=y/(x+y+z)

        return x,y
        

    def __load_color_data_from_csv(self):
        print('Load Color Data from CSV Start')
        with open('temp_data/color.csv','r') as f:
            reader=csv.reader(f,delimiter=',')
            for row in reader:
                self.xy.append([float(s) for s in row])
        self.xy=np.array(self.xy)
        print('Load Color Data from CSV End')


    def __load_brightness_data_from_csv(self):
        print('Load Brightness Data from CSV Start')
        with open('temp_data/brightness.csv','r') as f:
            reader=csv.reader(f,delimiter=',')
            i=0
            for row in reader:
                self.brightness[i]=[float(s) for s in row]
                i+=1
        print('Load Brightness Data from CSV End')

    def __load_brightness_data_from_video_from_csv(self):
        print('Load Brightness Data from Video from CSV Start')
        with open('temp_data/brightness_from_video.csv','r') as f:
            reader=csv.reader(f,delimiter=',')
            for row in reader:
                self.brightness_from_video=row
        print('Load Brightness Data from Video from CSV Start')