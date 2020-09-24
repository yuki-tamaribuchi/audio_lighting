from DataProcessing import DataProcessing
from Player import Player
import time

#実装サンプル

file='file.mp4'

#audio->'a',video->'v'
dp1=DataProcessing(file,'v')
#dp1.create_brightness_data()

pl1=Player(file=file,audio_len=dp1.audio_time_length,color_data=dp1.color_x_left)
pl1.play_w_lightring()
