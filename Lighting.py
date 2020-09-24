from phue import Bridge
import time

class Lighting():

    def __init__(self,ip_addr):
        self.b=Bridge(ip_addr)
        self.b.connect()
        #self.lights=b.lights
        #self.lights[0].brightness=127


    def brightness(self,data,audio_len):
        data_length=len(data)
        interval=audio_len/data_length
        print(interval)
        for i in range(0,data_length):
            start=time.time()
            #self.lights[0].brightness=127+(int(data[i])*30)
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
            #self.b.set_light(1,'color',data[i])
            print('left x=',data[0][i],'left y=',data[2][i],',right x=',data[1][i],',right y=',data[3][i])
            end=time.time()
            time.sleep(interval-(end-start))