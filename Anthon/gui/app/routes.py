import requests

from flask import Blueprint, render_template, current_app, request, redirect

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    videos = []

    if request.method == 'GET':
        video_url = "http://127.0.0.1:5001/users"
        r = requests.get(video_url)
        results = r.json()
        for result in results:
            video_data = {
                'user_id': result['user_id'],
                'username': result['username'],
                'url': f'http://127.0.0.1:5001/users/{result["user_id"]}',
            }
            videos.append(video_data)

    return render_template('index.html', videos=videos)
