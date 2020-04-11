import requests
from datetime import datetime
from flask import Blueprint, render_template, current_app, request, redirect

GUI_HOST = ""
GUI_PORT = ""
API_HOST = ""
API_PORT = ""

main = Blueprint('main', __name__)
GUI_URL = f'http://{GUI_HOST}:{GUI_PORT}'
API_URL = f'http://{API_HOST}:{API_PORT}'


@main.route('/', methods=['GET'])
def main_users():
    just_before()

    users = []

    if request.method == 'GET':
        main_url = f'{API_URL}/users'
        r = requests.get(main_url)
        results = r.json()

        for result in results:
            user_data = {
                'user_id': result['user_id'],
                'username': result['username'],
                'url': f'{GUI_URL}/users/{result["user_id"]}',
            }
            users.append(user_data)

    return render_template('index.html', users=users)


@main.route("/users/<int:user_id>", methods=['GET'])
def user_page(user_id):
    just_before()

    snapshots = []
    
    user_url = f'{API_URL}/users/{user_id}'
    r = requests.get(user_url)
    user_result = r.json()

    birthdate = user_result['birthdate']
    birthdate = datetime.utcfromtimestamp(int(birthdate)).strftime('%Y-%m-%d %H:%M:%S')

    user = {
        'user_id': user_id,
        'username': user_result['username'],
        'birthdate': birthdate,
        'gender': user_result['gender']
    }

    snapshots_url = f'{API_URL}/users/{user_id}/snapshots'
    r = requests.get(snapshots_url)
    snapshot_results = r.json()

    for result in snapshot_results:
        timestmap = result['timestamp']
        time = datetime.utcfromtimestamp(int(timestmap) / 1000).strftime('%Y-%m-%d %H:%M:%S')

        snapshot = {
            'snapshot_id': result['snapshot_id'],
            'snapshot_path': f'{GUI_URL}/users/{user_id}/snapshots/{result["snapshot_id"]}',
            'timestamp': timestmap,
            'time': time
        }
        snapshots.append(snapshot)
    snapshots = sorted(snapshots, key=lambda snp: int(snp['timestamp']))

    return render_template('user.html', user=user, snapshots=snapshots)


@main.route("/users/<int:user_id>/snapshots/<snapshot_id>", methods=['GET'])
def snapshot_page(user_id, snapshot_id):
    just_before()

    snapshot_url = f'{API_URL}/users/{user_id}/snapshots/{snapshot_id}'
    r = requests.get(snapshot_url)
    result = r.json()

    user = {
        'user_id': user_id
    }
    snapshot = {
        'snapshot_id': snapshot_id
    }

    urls = {}
    pose = False
    feelings = False
    color_image = False
    depth_image = False
    pose_data = ""
    feelings_data = ""
    pose_data_formatted = ""
    feelings_data_formatted = ""

    if 'pose' in result:
        pose = True
        urls['pose'] = f'{API_URL}/users/{user_id}/snapshots/{snapshot_id}/pose'
        pose_data = result['pose']
        pose_data_formatted = {}
        for k, v in pose_data.items():
            pose_data_formatted[k] = float("{:.4f}".format(v))

    if 'feelings' in result:
        feelings = True
        urls['feelings'] = f'{API_URL}/users/{user_id}/snapshots/{snapshot_id}/feelings'
        feelings_data = result['feelings']
        feelings_data_formatted = {}
        for k, v in feelings_data.items():
            feelings_data_formatted[k] = float("{:.4f}".format(v))

    if 'color_image' in result:
        color_image = True
        urls['color_image'] = f'{API_URL}/users/{user_id}/snapshots/{snapshot_id}/color_image/data'

    if 'depth_image' in result:
        depth_image = True
        urls['depth_image'] = f'{API_URL}/users/{user_id}/snapshots/{snapshot_id}/depth_image/data'

    return render_template('snapshot.html', pose=pose, feelings=feelings,
                           depth_image=depth_image, color_image=color_image, urls=urls,
                           user=user, snapshot=snapshot, pose_data=pose_data_formatted, feelings_data=feelings_data_formatted)


def just_before():
    global GUI_HOST, GUI_PORT, API_HOST, API_PORT, GUI_URL, API_URL

    GUI_HOST = current_app.config['host']
    GUI_PORT = current_app.config['port']
    API_HOST = current_app.config['api_host']
    API_PORT = current_app.config['api_port']
    GUI_URL = f'http://{GUI_HOST}:{GUI_PORT}'
    API_URL = f'http://{API_HOST}:{API_PORT}'
