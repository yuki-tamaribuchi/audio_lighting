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
    chroma_array_rihgt=[]
    brightness_left=[]
    brightness_right=[]


    def __init__(self,file):
        self.load_music(file)
        self.hpss_execute()
        self.chromacqt_execute()
        self.create_io_array()


    def load_music(self,file):
        print('Loading Start')
        self.rate,self.loaded_data=wavfile.read(file)
        self.normalized_data=self.loaded_data/32768
        print('Loading End')
        

    def hpss_execute(self):
        print('HPSS Start')
        self.hpss_harmonics_left,self.hpss_percussion_left=librosa.effects.hpss(self.normalized_data[:,0])
        self.hpss_harmonics_right,self.hpss_percussion_right=librosa.effects.hpss(self.normalized_data[:,1])


    def chromacqt_execute(self,hop_length=2048,n_octaves=2,n_chroma=12):
        print('Chroma CQT Start')
        self.chrcqt_left_data=librosa.feature.chroma_cqt(y=self.hpss_harmonics_left,sr=self.rate,hop_length=hop_length,n_octaves=n_octaves,n_chroma=n_chroma)
        self.chrcqt_right_data=librosa.feature.chroma_cqt(y=self.hpss_harmonics_right,sr=self.rate,hop_length=hop_length,n_octaves=n_octaves,n_chroma=n_chroma)
        print('Chroma CQT End')

    
    def disp_chrcqt(self,data,hop_length=2048):
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
        print(self.brightness_left.shape)
        