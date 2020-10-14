import matplotlib.pyplot as plt
import csv

class PaperData():

    def __init__(self,instance):
        self.instance=instance

    def create_chroma_array(self):
        self.chroma_left=[]
        self.chroma_right=[]
        scale=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

        left=self.instance._DataProcessing__cens_left.real.argmax(axis=0)
        right=self.instance._DataProcessing__cens_right.real.argmax(axis=0)

        for i in left:
            self.chroma_left.append(scale[i])
        for i in right:
            self.chroma_right.append(scale[i])

    def save_chroma_array(self):
        chroma_scale=[[self.chroma_left],[self.chroma_right]]
        with open('chroma_scale.csv','w') as f:
            writer=csv.writer(f)
            writer.writerows(chroma_scale)



