from DataProcessing import DataProcessing
from Player import Player
import time


#実装サンプル

file='media_file/rojo.mp4'

#audio->'a',video->'v'
dp1=DataProcessing(file,'v',True)

pl1=Player(file,dp1)
pl1.play()
