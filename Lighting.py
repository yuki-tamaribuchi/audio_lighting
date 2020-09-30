from phue import Bridge
import time

class Lighting():

    def __init__(self,ip_addr):
        self.b=Bridge(ip_addr)
        self.b.connect()
        self.lights=self.b.lights
        self.lights[2].brightness=127


    def brightness(self,data,audio_time_length):
        data_length=len(data)
        interval=audio_time_length/data_length
        print('Brightness Interval=',interval)
        for i in range(0,data_length):
            start=time.time()
            #self.lights[0].brightness=127+(int(data[i])*30)
            cmd={
                'bri':int(255*data[i]),
                'transitiontime':0,
            }
            self.b.set_light(3,cmd)
            print(data[i])
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