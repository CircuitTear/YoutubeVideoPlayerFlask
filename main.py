from flask import Flask, request, redirect, send_file
from flask_cors import CORS
from pytubefix import YouTube
import pytubefix

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app)

@app.route('/')
def index():
    return redirect("https://github.com/Egg-RecRoom/YoutubeVideoPlayerFlask")

@app.route('/api/video')
def apivideo():
    url = request.args.get('url')
    if not url:
        return 'Missing url', 400
    try:
        video = YouTube(url).streams.get_highest_resolution(progressive=True)
    except pytubefix.exceptions.AgeRestrictedError:
        return "Age restricted"
    except pytubefix.exceptions.VideoUnavailable:
        return "Video unavailable"
    except pytubefix.exceptions.RegexMatchError:
        return "could not find match for " + str(url)
    
    video.download(filename="temp.mp4")

    return send_file("temp.mp4")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)