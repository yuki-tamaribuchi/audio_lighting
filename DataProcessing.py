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

import sys
np.set_printoptions(threshold=sys.maxsize)

class DataProcessing():


    loaded_data=[]
    normalized_data=[]
    hpss_harmonics_left=[]
    hpss_harmonics_right=[]
    hpss_percussion_left=[]
    hpss_percussion_right=[]
    chrcqt_left_data=[]
    chrcqt_right_data=[]
    cens_left=[[],[],[],[],[],[],[],[],[],[],[],[]]
    cens_right=[[],[],[],[],[],[],[],[],[],[],[],[]]
    rate=0
    audio_time_length=0
    chroma_array_left=[]
    chroma_array_right=[]
    brightness=[[],[]]
    brightness_from_video=[]
    


    color_array=[[],[],[],[]]


    def __init__(self,file,mode):

        if mode=='a':
            self.load_music(file)
            if self.check_temp():

                self.load_cens()
                self.create_color_data()


                self.load_color_data_from_csv()
                self.load_brightness_data_from_csv()
            else:
#                self.dump_audio_array_length()
#                #self.estimate_bpm()
#                self.hpss_execute()
#                self.chromacens_execute()
#                self.create_brightness_data()
#                self.save_brightness_data()
#
#                self.export_csv()
                self.load_cens()
                self.create_color_data()
#                self.save_color_data()
        elif mode=='v':
            self.load_audio_from_video(file)
            if self.check_temp():


                self.load_cens()
                self.create_rgb_data()




                self.load_color_data_from_csv()
                self.load_brightness_data_from_csv()
                #self.load_brightness_data_from_video_from_csv()
            else:
                    
                self.dump_audio_array_length()
                #self.estimate_bpm()
                self.hpss_execute()
                self.chromacens_execute()
                self.create_brightness_data()
                self.save_brightness_data()
                
                self.export_csv()
                
                self.create_rgb_data()

                
                self.save_color_data()
                #self.calc_brightness_from_video(file)
                #self.save_brightness_from_video_data()
                
        else:
            print('モードを"a"，または"v"で指定してください')



    def load_music(self,file):
        print('Loading Start')
        self.rate,self.loaded_data=wavfile.read(file)
        self.normalized_data=self.loaded_data/32768
        #self.dump_audio_array_length()
        self.audio_time_length=len(self.normalized_data)/self.rate
        print('Loading End')


    def load_audio_from_video(self,file):
        print('Loading Start')
        video_data=VideoFileClip(file)
        audio_data=video_data.audio
        self.normalized_data=audio_data.to_soundarray()
        self.rate=44100
        #self.dump_audio_array_length()
        self.audio_time_length=len(self.normalized_data)/self.rate
        print('Loading End')


    def estimate_bpm(self):
        print('Estimate BPM Start')
        self.bpm=librosa.beat.tempo(y=self.normalized_data[:,0])
        print('Estimate BPM End')
        print('BPM=',self.bpm)
        

    def hpss_execute(self):
        print('HPSS Start')
        self.hpss_harmonics_left,self.hpss_percussion_left=librosa.effects.hpss(self.normalized_data[:,0])
        self.hpss_harmonics_right,self.hpss_percussion_right=librosa.effects.hpss(self.normalized_data[:,1])
        print('HPSS End')


    def chromacqt_execute(self,hop_length=2048,n_octaves=2,n_chroma=12):
        print('Chroma CQT Start')
        self.chrcqt_left_data=librosa.feature.chroma_cqt(y=self.hpss_harmonics_left,sr=self.rate,hop_length=hop_length,n_octaves=n_octaves,n_chroma=n_chroma)
        self.chrcqt_right_data=librosa.feature.chroma_cqt(y=self.hpss_harmonics_right,sr=self.rate,hop_length=hop_length,n_octaves=n_octaves,n_chroma=n_chroma)
        print('Chroma CQT End')


    def chromacens_execute(self,n_bins=48,hop_length=4096,fmin=130.813,win_len_smooth=20):
        print('Chroma Cens Start')
        C_left=librosa.cqt(self.hpss_harmonics_left,n_bins=n_bins,hop_length=hop_length)
        C_right=librosa.cqt(self.hpss_harmonics_right,n_bins=n_bins,hop_length=hop_length)
        self.cens_left=librosa.feature.chroma_cens(C=C_left,hop_length=hop_length,fmin=fmin,win_len_smooth=win_len_smooth)
        self.cens_right=librosa.feature.chroma_cens(C=C_right,hop_length=hop_length,fmin=fmin,win_len_smooth=win_len_smooth)
        print('Chroma Cens End')
    

    def disp_chrcqt(self,data,hop_length=4096):
        plt.figure(figsize=(15,5))
        librosa.display.specshow(data,x_axis='time',y_axis='chroma',hop_length=hop_length,cmap='coolwarm')
        plt.show()

    def dump_audio_array_length(self):
        d={'length':len(self.normalized_data)}
        with open('temp_data/temp.json','w') as f:
            json.dump(d,f)

    def check_temp(self):
        if not os.path.isfile('temp_data/temp.json'):
            return False
        with open('temp_data/temp.json','r') as f:
            temp_data=json.load(f)
            print(temp_data['length']==len(self.normalized_data))
            return temp_data['length']==len(self.normalized_data)
                


    def export_csv(self):
        print('Export Start')
        with open('temp_data/data.csv','w') as f:
            writer=csv.writer(f)
            writer.writerows(self.cens_left)
        print('Export End')

    def save_color_data(self):
        print('Save Color Data Start')
        with open('temp_data/color.csv','w') as f:
            writer=csv.writer(f)
            writer.writerows(self.color_array)
        print('Save Color Data End')


    def save_brightness_data(self):
        print('Save Brightness Data Start')
        with open('temp_data/brightness.csv','w') as f:
            writer=csv.writer(f)
            writer.writerows(self.brightness)
        print('Save Brightness Data End')


    def save_brightness_from_video_data(self):
        print('Save Brightness from Video Data Start')
        with open('temp_data/brightness_from_video.csv','w') as f:
            writer=csv.writer(f)
            writer.writerow(self.brightness_from_video)
        print('Save Brightness from Video Data Start')

    
    def create_brightness_data(self):
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


    def calc_brightness_from_video(self,file):
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




    def create_rgb_data(self):
        print('Create RGB Data Start')
        #convert sRGB to CIE1931 XY


        chroma_rgb=np.array([
            #C
            [50,0,0],

            #C#
            [150,150,150],

            #D
            [200,190,100],

            #D#
            [0,100,65],

            #E
            [0,130,65],

            #F
            [200,0,30],

            #F#
            [230,190,190],

            #G
            [255,255,190],

            #G#
            [240,240,240],

            #A
            [150,100,50],

            #A#
            [120,0,130],

            #B
            [230,150,190]
        ])



        #時間ごとの音階の合計を計算
        left_cens_total_by_time=self.cens_left.real.sum(axis=0)
        #right_cens_total_by_time=self.cens_right.real.sum(axis=0)

        #時間ごとの音階の割合を計算
        left_normalized_by_time=np.nan_to_num(np.divide(self.cens_left.real,left_cens_total_by_time))
        #right_normalized_by_time=np.nan_to_num(np.divide(self.cens_right.real,right_cens_total_by_time))

        #3回repeatしてreshape
        left_normalized_by_time=np.repeat(left_normalized_by_time,3).reshape(12,len(left_normalized_by_time[0]),3)
        #right_normalized_by_time=np.repeat(right_normalized_by_time,3).reshape(12,len(right_normalized_by_time[0]),3)


        #normalized_by_timeのlength回繰り返してreshape
        chroma_rgb=np.repeat(chroma_rgb,len(left_normalized_by_time[0]),0).reshape(12,len(left_normalized_by_time[0]),3)


        left_rgb_mean=np.multiply(left_normalized_by_time,chroma_rgb)
        #right_rgb_mean=np.multiply(right_normalized_by_time,chroma_rgb)


        left_rgb_total=left_rgb_mean.sum(axis=0)
        #right_rgb_total=right_rgb_mean.sum(axis=0)

        






        '''
        # gamma correction
        #R/256が0.04045より大きいか小さいか
        #大きければ2.4乗，小さければ12.92で割るだけ
        red_left = pow( ((rgb_left['R']/256) + 0.055) / (1.0 + 0.055), 2.4 ) if (rgb_left['R']/256) > 0.04045 else ((rgb_left['R']/256) / 12.92)



        green_left = pow(((rgb_left['G']/256) + 0.055) / (1.0 + 0.055), 2.4) if (rgb_left['G']/256) > 0.04045 else ((rgb_left['G']/256) / 12.92)


        blue_left =  pow(((rgb_left['B']/256) + 0.055) / (1.0 + 0.055), 2.4) if (rgb_left['B']/256) > 0.04045 else ((rgb_left['B']/256) / 12.92)

        red_right = pow(((rgb_right['R']/256) + 0.055) / (1.0 + 0.055), 2.4) if (rgb_right['R']/256) > 0.04045 else ((rgb_right['R']/256) / 12.92)
        green_right = pow(((rgb_right['G']/256) + 0.055) / (1.0 + 0.055), 2.4) if (rgb_right['G']/256) > 0.04045 else ((rgb_right['G']/256) / 12.92)
        blue_right =  pow(((rgb_right['B']/256) + 0.055) / (1.0 + 0.055), 2.4) if (rgb_right['B']/256) > 0.04045 else ((rgb_right['B']/256) / 12.92)

        # convert rgb to xyz
        x_left = red_left * 0.649926 + green_left * 0.103455 + blue_left * 0.197109
        y_left = red_left * 0.234327 + green_left * 0.743075 + blue_left * 0.022598
        z_left = green_left * 0.053077 + blue_left * 1.035763

        x_right = red_right * 0.649926 + green_right * 0.103455 + blue_right * 0.197109
        y_right = red_right * 0.234327 + green_right * 0.743075 + blue_right * 0.022598
        z_right = green_right * 0.053077 + blue_right * 1.035763

        # convert xyz to xy
        color_x_left.append(x_left / (x_left + y_left + z_left))
        color_y_left.append(y_left / (x_left + y_left + z_left))

        color_x_right.append(x_right / (x_right + y_right + z_right))
        color_y_right.append(y_right / (x_right + y_right + z_right))


        self.color_array[0]=color_x_left
        self.color_array[1]=color_x_right
        self.color_array[2]=color_y_left
        self.color_array[3]=color_y_right
        '''
        print('Create RGB Data End')
        
            


    def load_color_data_from_csv(self):
        print('Load Color Data from CSV Start')
        with open('temp_data/color.csv','r') as f:
            reader=csv.reader(f,delimiter=',')
            i=0
            for row in reader:
                self.color_array[i]=[float(s) for s in row]
                i+=1
        print('Load Color Data from CSV End')


    def load_brightness_data_from_csv(self):
        print('Load Brightness Data from CSV Start')
        with open('temp_data/brightness.csv','r') as f:
            reader=csv.reader(f,delimiter=',')
            i=0
            for row in reader:
                self.brightness[i]=[float(s) for s in row]
                i+=1
        print('Load Brightness Data from CSV End')

    def load_brightness_data_from_video_from_csv(self):
        print('Load Brightness Data from Video from CSV Start')
        with open('temp_data/brightness_from_video.csv','r') as f:
            reader=csv.reader(f,delimiter=',')
            for row in reader:
                self.brightness_from_video=row
        print('Load Brightness Data from Video from CSV Start')
            


    def load_cens(self):
        with open('temp_data/data.csv','r') as f:
            reader=csv.reader(f)
            i=0
            for row in reader:
                fl_row=[complex(s) for s in row]
                self.cens_left[i]=np.array(fl_row)
                i+=1
            
            self.cens_left=np.array(self.cens_left)