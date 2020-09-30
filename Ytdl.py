from pytube import YouTube


class Ytdl():
    
    def __init__(self,url):
        self.dl(url)


    def dl(self,url):
        yt=YouTube(url)
        print(yt.streams)