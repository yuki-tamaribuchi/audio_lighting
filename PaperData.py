import matplotlib.pyplot as plt
import numpy as np

class PaperData():

    def __init__(self,instance,verbose=None):
        self.instance=instance
        self.verbose=verbose

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
        import csv
        chroma_scale=[[self.chroma_left],[self.chroma_right]]

        if self.verbose:
            with open('chroma_scale_'+self.verbose+'.csv','w') as f:
                writer=csv.writer(f)
                writer.writerows(chroma_scale)
        else:
            with open('chroma_scale.csv','w') as f:
                writer=csv.writer(f)
                writer.writerows(chroma_scale)


    def save_logc_plot(self):
        import librosa
        import librosa.display
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

        fig_left=plt.Figure()
        canvas_left=FigureCanvas(fig_left)
        ax_left=fig_left.add_subplot(111)
        p_left=librosa.display.specshow(librosa.amplitude_to_db(self.instance._DataProcessing__C_left,ref=np.max),ax=ax_left,y_axis='log',x_axis='time')
        if self.verbose:
            fig_left.savefig('spec_left_'+self.verbose+'.png')
        else:
            fig_left.savefig('spec_left.png')

        fig_right=plt.Figure()
        canvas_right=FigureCanvas(fig_right)
        ax_right=fig_right.add_subplot(111)
        p_right=librosa.display.specshow(librosa.amplitude_to_db(self.instance._DataProcessing__C_right,ref=np.max),ax=ax_right,y_axis='log',x_axis='time')
        if self.verbose:
            fig_left.savefig('spec_right_'+self.verbose+'.png')
        else:
            fig_left.savefig('spec_right.png')

