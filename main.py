from flask import Flask, request, redirect, Response, send_file
import requests
from pytubefix import YouTube
import pytubefix

app = Flask(__name__)

@app.route('/')
def index():
    return redirect("https://github.com/Egg-RecRoom/YoutubeVideoPlayerFlask")

@app.route('/api/video')
def apivideo():
    url = request.args.get('url')
    if not url:
        return 'Missing url', 400
    try:
        video = YouTube(url).streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()
    except pytubefix.exceptions.AgeRestrictedError:
        return "Age restricted"
    except pytubefix.exceptions.VideoUnavailable:
        return "Video unavailable"
    except pytubefix.exceptions.RegexMatchError:
        return "could not find match for " + str(url)
    
    video.download(filename="temp.mp4")

    with open("temp.mp4", "rb") as f:
        videod = f.read()

    return Response(videod, 200, mimetype="video/mp4")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)