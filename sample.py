from ChromaCqt import ChromaCqt
from Player import Player
import time

#実装サンプル
cc1=ChromaCqt('file.wav')

pl1=Player(cc1.loaded_data[:,0],cc1.rate,cc1.io_array)
pl1.play_w_lightring()

