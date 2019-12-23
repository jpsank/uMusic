from app import app

from app.scrape.util import *

import requests, os
import re


CONSTANT_PARAMS = {
    'client_id': app.config['SOUNDCLOUD_CLIENT_ID']
}


def request_api(url, params=None):
    if params is None:
        params = {}
    params.update(CONSTANT_PARAMS)

    return requests.get(url, params)


def download_charts(kind='top', genre='danceedm', region='US', limit=100):
    url = "https://api-v2.soundcloud.com/charts"
    params = {
        'kind': kind,
        'genre': 'soundcloud:genres:{}'.format(genre),
        'region': 'soundcloud:regions:{}'.format(region),
        'limit': limit,
        'app_version': 1576752087
    }
    res = request_api(url, params)
    charts_json = res.json()
    for item in charts_json['collection']:
        t_track = minimize_track(item['track'])

        if len(t_track['media']['transcodings']) == 0:
            print('INFO: No valid transcodings for ["{}"]'.format(t_track['title']))
            continue

        download_track(t_track)


def minimize_track(track):

    artist = None
    album = None
    if track.get('publisher_metadata'):
        artist = track['publisher_metadata'].get('artist')
        album = track['publisher_metadata'].get('album')

    if not artist:
        artist = track['user'].get('full_name')
    if not artist:
        artist = track['user']['username']

    transcodings = []
    for tc in track['media']['transcodings']:
        protocol = tc['format']['protocol']
        if protocol == 'progressive':
            transcodings.append({
                'url': tc['url']
            })

    t_track = {
        'title': track['title'],
        'user': {'username': track['user']['username']},
        'release_date': track['release_date'],
        'genre': track['genre'],
        'artwork_url': track['artwork_url'],
        'media': {'transcodings': transcodings},
        'album': album,
        'artist': artist
    }
    return t_track


def download_track(t_track):
    # Folder and sub-folder names
    folder = os.path.join(app.config['SOUNDCLOUD_FOLDER'], sanitize_filename(t_track['artist']))
    mkdir_if_not_exists(folder)
    if t_track['album']:
        folder = os.path.join(folder, sanitize_filename(t_track['album']))
        mkdir_if_not_exists(folder)

    # File name
    filename = sanitize_filename(t_track['title'] + '.mp3')

    # Full path
    filepath = os.path.join(folder, filename)

    # Check if already exists
    if os.path.exists(filepath):
        print('INFO: Download aborted, file already exists [{}]'.format(filepath))
        return False

    print('INFO: Downloading track ["{}"]'.format(t_track['title']))

    # Request download url for transcoding
    transcoding_url = t_track['media']['transcodings'][0]['url']
    res = request_api(transcoding_url)
    j = res.json()

    # Download and save file
    download_url = j['url']
    res = requests.get(download_url)
    with open(filepath, 'wb') as f:
        f.write(res.content)

    tagged = tag_file(filepath,
                      artist=t_track['user']['username'],
                      title=t_track['title'],
                      date=t_track['release_date'],
                      genre=t_track['genre'],
                      album=t_track['album'],
                      artwork_url=t_track['artwork_url'])
    if not tagged:
        print('WARNING: Unable to tag file [{}]'.format(filepath))

    return True

