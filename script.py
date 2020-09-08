import numpy as np
import librosa
import librosa.display
from matplotlib import pyplot as plt
from scipy.io import wavfile

class AudioLighting():

    loaded_data=[]
    lr_separated_data={}
    cut_data=[]
    hpss_data={}
    chrcqt_data=[]
    rate=0

    def __init__(self):
        pass


    def load_music(self,file):
        print('Loading Start')
        rate,data=wavfile.read(file)
        data=data/32768
        self.rate=rate
        self.loaded_data = data
        print('Loading End')


    def cut(self,data,start,end):
        print('Cutting Start')
        self.cut_data=data[(start*self.rate):(end*self.rate),:]
        print('Cutting End')
        
    
    def lr_separate(self,data):
        print('Separating Start')
        self.lr_separated_data={'left':data[:,0],'right':data[:,1]}
        print('Separating End')

    def hpss_execute(self,data):
        print('HPSS Start')
        harmonic,percussive=librosa.effects.hpss(data)
        self.hpss_data={'harmonic':harmonic,'percussive':percussive}
        print('HPSS End')

    #def chromacqt_execute(self,data,hop_length,n_octaves=2,n_chroma=24):
    #    chrcqt=librosa.feature.chroma_cqt(y=data,sr=)
        

    

al1=AudioLighting()
al1.load_music('file.wav')
al1.cut(al1.loaded_data,10,20)
al1.lr_separate(al1.cut_data)
al1.hpss_execute(al1.lr_separated_data['left'])
print(al1.hpss_data['harmonic'])