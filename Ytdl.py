from pytube import YouTube

'''
20201001現在
音楽系データダウンロードするには，pytubeライブラリのextract.pyを改変(自己責任)
cipher_url = [
    parse_qs(formats[i]["signatureCipher"]) for i, data in enumerate(formats)
]
'''




class Ytdl():
    
    def __init__(self,url,filename):
        self.dl(url,filename)


    def dl(self,url,filename):
        print('Download Video from YouTube Start')
        yt=YouTube(url)
        yt.streams.all()
        #yt.streams.filter(progressive=True,file_extension='.mp4',res='1080p').order_by('resolution')[-1].download(output_path='from_yt',filename=filename)
        print('Download Video from YouTube End')


Ytdl('https://www.youtube.com/watch?v=qQjMMEWaWsc','these_nights')