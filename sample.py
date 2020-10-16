from DataProcessing import DataProcessing
from PaperData import PaperData
from Player import Player
from Lighting import Lighting
import time


#実装サンプル

file='media_file/rojo.mp4'

#audio->'a',video->'v'
dp1=DataProcessing(file,'v',True)

pd=PaperData(dp1)
pd.create_chroma_array()
pd.left_cens_plot()
pd.right_cens_plot()

#lt1=Lighting('192.168.11.99')

#pl1=Player(file,dp1,lt1)
#pl1.play()
