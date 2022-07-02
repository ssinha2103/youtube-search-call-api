import os

from flask import Flask, Blueprint, render_template, request, redirect
import requests
from isodate import parse_duration

import settings

app = Flask(__name__)


# main = Blueprint('main', "__name__")


@app.route('/', methods=['GET', 'POST'])
def index(config_file='settings.py'):  # put application's code here
    video_ids = []
    video_data = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        search_params = {
            'key': 'AIzaSyCT6bsRM44EqTzCrXCEM6MtX8fMhx9UTaA',
            'q': request.form.get('query'),
            'part': 'snippet',
            'maxResults': 9,
            'type': 'video'
        }
        search_results = requests.get(search_url, params=search_params)
        results_items = search_results.json()['items']
        [video_ids.append(item['id']['videoId']) for item in results_items]
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        video_params = {
            'key': 'AIzaSyCT6bsRM44EqTzCrXCEM6MtX8fMhx9UTaA',
            'id': ','.join(video_ids),
            'part': 'snippet, contentDetails',
            'maxResults': 9,
        }
        video_results = requests.get(video_url, params=video_params)
        video_results = video_results.json()['items']
        for results in video_results:
            video_info = {
                'id': results['id'],
                'url': f'https://www.youtube.com/watch?v={results["id"]}',
                'thumbnail': results['snippet']['thumbnails']['high']['url'],
                'duration': f"{int((parse_duration(results['contentDetails']['duration']).total_seconds()//60))} minutes",
                'title': results['snippet']['title'],
            }
            video_data.append(video_info)
        if request.form.get('submit')=='lucky':
            return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')
    return render_template('index.html', videos=video_data)


if __name__ == '__main__':
    app.run()
