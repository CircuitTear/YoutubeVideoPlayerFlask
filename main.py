from flask import Flask, request, redirect
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
        return "this video is age restricted"
    except pytubefix.exceptions.VideoUnavailable:
        return "this video is is unavailable"
    except pytubefix.exceptions.RegexMatchError:
        return "could not find match for " + str(url)
    video = video["adaptiveFormats"][0]

    return redirect(video["url"])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)