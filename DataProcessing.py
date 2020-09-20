import numpy as np
import librosa
import librosa.display
from matplotlib import pyplot as plt
from scipy.io import wavfile
import csv

class DataProcessing():


    loaded_data=[]
    normalized_data=[]
    hpss_harmonics_left=[]
    hpss_harmonics_right=[]
    hpss_percussion_left=[]
    hpss_percussion_right=[]
    chrcqt_left_data=[]
    chrcqt_right_data=[]
    rate=0
    chroma_array_left=[]
    chroma_array_right=[]
    brightness_left=[]
    brightness_right=[]


    def __init__(self,file):
        self.load_music(file)
        self.estimate_bpm()
        self.hpss_execute()
        self.chromacens_execute()
        self.create_io_array()


    def load_music(self,file):
        print('Loading Start')
        self.rate,self.loaded_data=wavfile.read(file)
        self.normalized_data=self.loaded_data/32768
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


    def export_csv(self):
        print('Export Start')
        with open('data.csv','w') as f:
            writer=csv.writer(f)
            writer.writerows(self.chrcqt_left_data,self.chrcqt_right_data)
        print('Export End')

    
    def create_io_array(self):
        self.chroma_array_left=np.where(self.chrcqt_left_data==1.0,1,0)
        self.chroma_array_left=np.where(self.chrcqt_right_data==1.0,1,0)


    def create_brightness_data(self):
        left_ave=abs(np.average(self.hpss_percussion_left))
        right_ave=abs(np.average(self.hpss_percussion_right))
        
        self.brightness_left=np.where(self.hpss_percussion_left>left_ave,1,0)
        self.brightness_right=np.where(self.hpss_harmonics_right>right_ave,1,0)

        

        self.brightness_left=self.brightness_left[::4410]
        

    def create_color_data(self):

        #convert sRGB to CIE1931 XY

        chroma_rgb={
            #C
            0:{
                'R':50,
                'G':0,
                'B':0,
            },
            #C#
            1:{
                'R':150,
                'G':150,
                'B':150,
            },
            #D
            2:{
                'R':200,
                'G':190,
                'B':100,
            },
            #D#
            3:{
                'R':0,
                'G':100,
                'B':65,
            },
            #E
            4:{
                'R':0,
                'G':130,
                'B':65,
            },
            #F
            5:{
                'R':200,
                'G':0,
                'B':30,
            },
            #F#
            6:{
                'R':230,
                'G':190,
                'B':190,
            },
            #G
            7:{
                'R':255,
                'G':255,
                'B':190,
            },
            #G#
            8:{
                'R':240,
                'G':240,
                'B':240,
            },
            #A
            9:{
                'R':150,
                'G':100,
                'B':50,
            },
            #A#
            10:{
                'R':120,
                'G':0,
                'B':130,
            },
            #B
            11:{
                'R':230,
                'G':150,
                'B':190,
            }
        }

        rgb_left=chroma_rgb[self.chroma_array_left]
        rgb_right=chroma_rgb[self.chroma_array_right]


        # gamma correction
        red_left = pow(((rgb_left['R']/256) + 0.055) / (1.0 + 0.055), 2.4) if (rgb_left['R']/256) > 0.04045 else ((rgb_left['R']/256) / 12.92)
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
        self.x_left = x_left / (x_left + y_left + z_left)
        self.y_left = y_left / (x_left + y_left + z_left)
        
        self.x_right = x_right / (x_right + y_right + z_right)
        self.y_right = y_right / (x_right + y_right + z_right)
    