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
        if start>end:
            print('error...end sec is shorter than start sec')
            exit()
        else:
            print('Cutting Start')
            self.cut_data=data[(start*self.rate):(end*self.rate),:]
            print('Cutting End')
        
    
    def lr_separate(self,data):
        print('Separating Start')
        self.lr_separated_data={'left':data[:,0],'right':data[:,1]}
        print('Separating End')

    def hpss_execute(self,data,l_or_r=None):
        print('HPSS Start')
        if l_or_r == None:
            left_harmonic,left_percussive=librosa.effects.hpss(data['left'])
            right_harmonic,right_percussive=librosa.effects.hpss(data['right'])
            self.hpss_data={'left':{'harmonic':left_harmonic,'percussive':left_percussive},'right':{'harmonic':right_harmonic,'percussive':right_percussive}}
        else:
            harmonic,percussive=librosa.effects.hpss(data[l_or_r])
            self.hpss_data={'harmonic':harmonic,'percussive':percussive}
        print('HPSS End')

    def chromacqt_execute(self,data,chroma_mode='harmonic',hop_length=512,n_octaves=2,n_chroma=12):
        print('Chroma CQT Start')
        self.chrcqt_data=librosa.feature.chroma_cqt(y=data,sr=self.rate,hop_length=hop_length,n_octaves=n_octaves,n_chroma=n_chroma)
        print('Chroma CQT End')





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


    

al1=AudioLighting()
al1.load_music('file.wav')
al1.cut(al1.loaded_data,10,5)
al1.lr_separate(al1.cut_data)
al1.hpss_execute(al1.lr_separated_data,'right')
al1.chromacqt_execute(al1.hpss_data['harmonic'])

print(al1.chrcqt_data)


al2=AudioLighting()
al2.full_execute('file.wav',20,25,'right')
print(al2.chrcqt_data)