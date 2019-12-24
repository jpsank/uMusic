from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, send_from_directory, session, make_response
from app import app, db
from sqlalchemy import func
from app.models import Track, Album, Artist
from app.main import bp
import os
import urllib.parse


# def paginate(items, per_page=app.config['TRACKS_PER_PAGE']):
#     page = request.args.get('page', 1, type=int)
#
#     items = items.paginate(page, per_page, False)
#
#     next_url = url_for(request.endpoint, page=items.next_num) if items.has_next else None
#     prev_url = url_for(request.endpoint, page=items.prev_num) if items.has_prev else None
#     return items, next_url, prev_url


# Front pages


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('home.html', title='Home')


def get_some_tracks(counter=0, quantity=app.config['TRACKS_PER_PAGE'], genre='all'):
    tracks = Track.query
    if genre != 'all':
        tracks = tracks.filter_by(genre=genre)
    tracks = tracks.offset(counter).limit(quantity)
    return tracks


@app.route('/load')
def load_more():
    # this route will be called from JavaScript when the page is scrolled
    counter = request.args.get('c', 0)
    tracks = get_some_tracks(counter)
    return jsonify([t.serialize() for t in tracks])


# Retrieve track audio and image files


def send_from_directory2(directory, filename):
    response = make_response(send_from_directory(directory, filename))
    response.headers["Content-Disposition"] = \
        "attachment; " \
        "filename*=UTF-8''{quoted_filename}".format(
            quoted_filename=urllib.parse.quote(filename.encode('utf8'))
        )
    return response


@bp.route('/play/<track_id>')
def play_track(track_id):
    track = Track.query.filter_by(id=track_id).first_or_404()
    return send_from_directory2(app.config['SOUNDCLOUD_FOLDER'], track.path)


@bp.route('/image/<track_id>')
def download_image(track_id):
    track = Track.query.filter_by(id=track_id).first_or_404()
    return send_from_directory2(app.config['SOUNDCLOUD_IMAGE_FOLDER'], track.image_path)

