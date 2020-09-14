from DataProcessing import DataProcessing
from Player import Player
from Lighting import Lighting
import time

#実装サンプル
'''
dp1=DataProcessing('file.wav')
dp1.create_brightness_data()

pl1=Player(dp1.loaded_data[:,0],dp1.rate,dp1.chroma_array_left)
pl1.play_w_lightring()

'''

lt1=Lighting('192.168.11.11')
lt1.brightness()