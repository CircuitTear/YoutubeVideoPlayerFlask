from flask import Flask, request, redirect, Response
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
        video = YouTube(url).streaming_data
    except pytubefix.exceptions.AgeRestrictedError:
        return "Age restricted"
    except pytubefix.exceptions.VideoUnavailable:
        return "Video unavailable"
    except pytubefix.exceptions.RegexMatchError:
        return "could not find match for " + str(url)
    video = video["adaptiveFormats"][0]
    videodata = requests.request("GET", video["url"], headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}, stream=True,)
    return Response(videodata.content, 200, mimetype="video/mp4")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)