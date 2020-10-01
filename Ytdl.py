from pytube import YouTube

'''
音楽系データダウンロードするには，pytubeライブラリのextract.pyを改変(自己責任)
cipher_url = [
    parse_qs(formats[i]["signatureCipher"]) for i, data in enumerate(formats)
]
'''




class Ytdl():
    
    def __init__(self,url):
        self.dl(url)


    def dl(self,url):
        print('Download Video from YouTube Start')
        yt=YouTube(url)
        print(yt.streams)
        print('Download Video from YouTube End')