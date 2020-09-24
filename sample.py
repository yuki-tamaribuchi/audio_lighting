from DataProcessing import DataProcessing
from Player import Player
import time

#実装サンプル

#audio->'a',video->'v'
dp1=DataProcessing('file.wav','a')
dp1.create_brightness_data()

pl1=Player(dp1.loaded_data[:,0],dp1.rate,dp1.chroma_array_left)
pl1.play_w_lightring(brightness_data=dp1.brightness_left,color_data=dp1.color_x_left)
