from phue import Bridge


class Lighting():

    def __init__(self,ip_addr):
        b=Bridge(ip_addr)
        b.connect()
        self.lights=b.lights

    def brightness(self,data=None):
        self.lights[0].brightness=127