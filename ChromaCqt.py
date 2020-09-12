import numpy as np
import librosa
import librosa.display
from matplotlib import pyplot as plt
from scipy.io import wavfile
import csv

class ChromaCqt():

    loaded_data=[]
    normalized_data=[]
    lr_separated_data={}
    cut_data=[]
    hpss_data={}
    chrcqt_data={}
    rate=0
    io_array=[]

    def __init__(self,file):
        self.load_music(file)
        self.lr_separate(self.normalized_data)
        self.hpss_execute(self.lr_separated_data)
        self.chromacqt_execute(self.hpss_data)


    def load_music(self,file):
        print('Loading Start')
        self.rate,self.loaded_data=wavfile.read(file)
        self.normalized_data=self.loaded_data/32768
        print('Loading End')
        
    
    def lr_separate(self,data):
        print('Separating Start')
        self.lr_separated_data={'left':data[:,0],'right':data[:,1]}
        print('Separating End')

    def hpss_execute(self,data):
        print('HPSS Start')
        left_harmonic,left_percussive=librosa.effects.hpss(data['left'])
        right_harmonic,right_percussive=librosa.effects.hpss(data['right'])
        self.hpss_data={'left':{'harmonic':left_harmonic,'percussive':left_percussive},'right':{'harmonic':right_harmonic,'percussive':right_percussive}}
        print('HPSS End')



    def chromacqt_execute(self,data,chroma_mode='harmonic',hop_length=512,n_octaves=2,n_chroma=12):
        print('Chroma CQT Start')
        self.chrcqt_data['left']=librosa.feature.chroma_cqt(y=data['left']['harmonic'],sr=self.rate,hop_length=hop_length,n_octaves=n_octaves,n_chroma=n_chroma)
        self.chrcqt_data['right']=librosa.feature.chroma_cqt(y=data['right']['harmonic'],sr=self.rate,hop_length=hop_length,n_octaves=n_octaves,n_chroma=n_chroma)

        print('Chroma CQT End')

    
    def disp_chrcqt(self,data,hop_length=512):
        plt.figure(figsize=(15,5))
        librosa.display.specshow(data,x_axis='time',y_axis='chroma',hop_length=hop_length,cmap='coolwarm')
        plt.show()



    
    def export_csv(self):
        print('Export Start')
        with open('data.csv','w') as f:
            writer=csv.writer(f)
            writer.writerows(self.chrcqt_data)
        print('Export End')


    def create_io_array(self):
        self.io_array=np.where(self.chrcqt_data==1.0,1,0)
        
        with open('io_array.csv','w') as f:
            writer=csv.writer(f)
            writer.writerows(self.io_array)



    '''
    実装一時停止
    def full_execute(self,file,start=None,end=None,l_or_r=None,chroma_mode='harmonic',hop_length='512',n_octaves=2,n_chroma=12):
        self.load_music(file)

        if not start == None and end == None:
            self.cut(self.loaded_data[(self.rate*start):(self.rate*end),:])


        if self.cut_data == []:
            self.lr_separate(self.loaded_data)
        else:
            self.lr_separate(self.cut_data)
        

        self.hpss_execute(self.lr_separated_data,l_or_r)
        self.chromacqt_execute(self.hpss_data,chroma_mode,hop_length,n_octaves,n_chroma)
        '''

