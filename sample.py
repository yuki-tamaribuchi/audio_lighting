from DataProcessing import DataProcessing
from Player import Player
import time

#実装サンプル

file='file.wav'

#audio->'a',video->'v'
dp1=DataProcessing(file,'a')

pl1=Player(file=file,audio_time_length=dp1.audio_time_length,color_data=dp1.color_array)
pl1.play_w_lightring()
