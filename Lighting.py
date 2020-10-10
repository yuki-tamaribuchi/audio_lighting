from phue import Bridge
import time
from scipy.signal import resample

class Lighting():

    def __init__(self,ip_addr):
        self.__b=Bridge(ip_addr)
        self.__b.connect()


    def brightness(self,data,audio_time_length,data_v=None):
        data_length=len(data[0])
        interval=audio_time_length/data_length
        print('Brightness Interval=',interval)

        if data_v:
            resampled_data_v=resample(data_v,data_length)
            for i in range(0,data_length):
                start=time.time()
                cmd={
                    'bri':int(127*data[0][i])+int(127*resampled_data_v[i]),
                    'transitiontime':0,
                }
                self.__b.set_light(3,cmd)
                print('v',' ',data[0][i],',',resampled_data_v[i])
                end=time.time()
                time.sleep(interval-(end-start))
        else:
            for i in range(0,data_length):
                start=time.time()
                #self.lights[0].brightness=127+(int(data[i])*30)
                cmd={
                    #一時的にleftを割り当て
                    'bri':int(255*data[0][i]),
                    'transitiontime':0,
                }
                self.__b.set_light(3,cmd)
                print('Brightness=',data[0][i])
                end=time.time()
                time.sleep(interval-(end-start))

    
    def color(self,data,audio_len):
        print(data.shape)
        data_length=len(data)
        print('Color Data Length=',data_length)
        interval=audio_len/data_length
        print('Color Interval=',interval,'sec')
        for i in range(0,data_length):
            start=time.time()
            cmd={
                'xy':(data[i][0],data[i][1]),
                'transitiontime':0,
            }
            self.__b.set_light(3,cmd)
            #self.lights[2].xy=data[0][i],data[2][i]
            print('left x=',data[i][0],',left y=',data[i][1],',right x=',data[i][2],',right y=',data[i][3])
            end=time.time()
            time.sleep(interval-(end-start))