from DataProcessing import DataProcessing
from Player import Player
import time


#実装サンプル

file='mirrors.mp4'

#audio->'a',video->'v'
dp1=DataProcessing(file,'v')

pl1=Player(file=file,audio_time_length=dp1.audio_time_length,color_data=dp1.color_array,brightness_data=dp1.brightness,brightness_v_data=dp1.brightness_from_video)
pl1.play_w_lightring()
