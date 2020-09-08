import numpy as np
import librosa
import librosa.display
from matplotlib import pyplot as plt
from scipy.io import wavfile

class AudioLighting():

    loaded_data={}
    lr_separated_data={}
    cut_data=[]
    hpss_data={}

    def __init__(self):
        pass


    def load_music(self,file):
        rate,data=wavfile.read(file)
        data=data/32768
        self.loaded_data = {'rate':rate,'data':data}


    def cut(self,data,start,end):
        self.cut_data=data[(start*self.loaded_data['rate']):(end*self.loaded_data['rate']),:]
        
    
    def lr_separate(self,data):
        self.lr_separated_data={'left':data[:,0],'right':data[:,1]}

    def hpss_execute(self,data):
        harmonic,percussive=librosa.effects.hpss(data)
        self.hpss_data={'harmonic':harmonic,'percussive':percussive}

    

al1=AudioLighting()
al1.load_music('file.wav')
al1.cut(al1.loaded_data['data'],10,20)
al1.lr_separate(al1.cut_data)
al1.hpss_execute(al1.lr_separated_data['left'])
print(al1.hpss_data['harmonic'])