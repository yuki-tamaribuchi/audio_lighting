import numpy as np
import librosa
import librosa.display
from matplotlib import pyplot as plt
from scipy.io import wavfile

class AudioLighting():

    loaded_data={}

    def __init__(self):
        pass


    def load_music(self,file):
        rate,data=wavfile.read(file)
        self.loaded_data = {'rate':rate,'data':data}

    
    #def hpss

    

al1=AudioLighting()
al1.load_music('file.wav')
print(al1.loaded_data['rate'])