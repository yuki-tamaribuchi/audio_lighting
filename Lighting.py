from phue import Bridge
import time
from scipy.signal import resample

class Lighting():

    def __init__(self,ip_addr):
        self.b=Bridge(ip_addr)
        self.b.connect()
        self.lights=self.b.lights
        self.lights[2].brightness=127


    def brightness(self,data,audio_time_length,data_v=None):
        data_length=len(data[0])
        interval=audio_time_length/data_length
        print('Brightness Interval=',interval)

        if data_v:
            resampled_data_v=resample(data_v,data_length)
        else:
            for i in range(0,data_length):
                start=time.time()
                #self.lights[0].brightness=127+(int(data[i])*30)
                cmd={
                    #一時的にleftを割り当て
                    'bri':int(255*data[0][i]),
                    'transitiontime':0,
                }
                self.b.set_light(3,cmd)
                print(data[0][i])
                end=time.time()
                time.sleep(interval-(end-start))

    
    def color(self,data,audio_len):
        data_length=len(data[0])
        print(data_length)
        interval=audio_len/data_length
        print('interval=',interval,'sec')
        for i in range(0,data_length):
            start=time.time()
            cmd={
                'xy':(data[0][i],data[2][i]),
                'transitiontime':0,
            }
            self.b.set_light(3,cmd)
            #self.lights[2].xy=data[0][i],data[2][i]
            print('left x=',data[0][i],',left y=',data[2][i],',right x=',data[1][i],',right y=',data[3][i])
            end=time.time()
            time.sleep(interval-(end-start))