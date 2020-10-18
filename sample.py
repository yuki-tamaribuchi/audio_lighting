from DataProcessing import DataProcessing
from Player import Player
from Lighting import Lighting
import time


#実装サンプル

file='media_file/piano_file/piano_only_bpm100_original.wav'

#audio->'a',video->'v'
dp1=DataProcessing(file,'a',True)
lt1=Lighting('192.168.11.99')

pl1=Player(file,dp1,lt1)
pl1.play()
