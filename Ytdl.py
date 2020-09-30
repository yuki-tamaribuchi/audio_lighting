from pytube import YouTube


class Ytdl():
    
    def __init__(self,url):
        self.dl(url)


    def dl(self,url):
        print('Download Video from YouTube Start')
        yt=YouTube(url)
        print(yt.streams)
        print('Download Video from YouTube End')