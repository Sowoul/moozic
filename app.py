from flask import Flask, render_template, request
from pytube import Search
from concurrent.futures import ThreadPoolExecutor
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

def grab_info(yt_obj):
    audio_url = yt_obj.streams.filter(only_audio=True).first().url
    return {
        'thumbnail': yt_obj.thumbnail_url,
        'title': yt_obj.title,
        'views': yt_obj.views,
        'creator': yt_obj.author,
        'audio_url': audio_url,
    }

@app.route('/home')
def run():
    return render_template('home.html')

@app.route('/', methods=["GET"])
def moz():
    song = request.args.get('search')
    video_info = []

    if song:
        cache_key = f'search_{song}'
        cached_result = cache.get(cache_key)

        if cached_result is not None:
            video_info = cached_result
        else:
            links = (Search(song).results)[:5]

            with ThreadPoolExecutor() as executor:
                video_info = list(executor.map(grab_info, links))

            cache.set(cache_key, video_info, timeout=60)

    return render_template('index.html', videos=video_info)

