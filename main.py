from flask import Flask, render_template, request
from pytube import YouTube, Search
from uuid import uuid1

app = Flask(__name__)

@app.route('/home')
def run():
    return render_template('home.html')

@app.route('/', methods=["GET"])
def moz():
    def grab_info(yt_obj):
        audio_url = (yt_obj.streams.filter(only_audio=True).first()).url
        return {
            'thumbnail': yt_obj.thumbnail_url,
            'title': yt_obj.title,
            'views': yt_obj.views,
            'creator': yt_obj.author,
            'audio_url': audio_url,
        }

    song = request.args.get('search')   
    
    if song:
        global links
        links = (Search(song).results)[:5]
        video_info = [grab_info(video) for video in links]
        return render_template('index.html', videos=video_info)
    
if __name__ == '__main__':
    app.run(port=8080)
