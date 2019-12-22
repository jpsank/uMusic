from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, send_from_directory, session
from app import app, db
from sqlalchemy import func
from app.models import Track, Album, Artist
from app.main import bp
import os


# def get_queue():
#     return session.get('queue')
#
#
# def set_queue(track_ids, i=0):
#     session['queue'] = [track_ids, i]
#
#
# def current_track():
#     queue = get_queue()
#     if queue is None:
#         return None
#
#     track_ids, i = queue
#     return Track.query.get(track_ids[i])
#
#
# def next_track():
#     track_ids, i = get_queue()
#     i = (i + 1) % len(track_ids)
#     set_queue(track_ids, i)
#
#
# def prev_track():
#     track_ids, i = get_queue()
#     i = (i - 1) % len(track_ids)
#     set_queue(track_ids, i)


# @bp.route('/')
# @bp.route('/index')
# def index():
#     if current_track() is None:
#         tracks = Track.query.all()
#         set_queue([track.id for track in tracks])
#     return render_template('home.html', title='Home', track=current_track())
#
#
# @bp.route('/next')
# def next_page():
#     next_track()
#     return redirect(url_for('main.index'))
#
#
# @bp.route('/prev')
# def prev_page():
#     prev_track()
#     return redirect(url_for('main.index'))


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


@bp.route('/tracks')
def show_tracks():
    tracks = get_some_tracks()
    return render_template('old/tracks.html', title='Tracks', tracks=tracks)


@app.route('/load')
def load_more():
    # this route will be called from JavaScript when the page is scrolled
    counter = request.args.get('c', 0)
    tracks = get_some_tracks(counter)
    return jsonify([t.serialize() for t in tracks])


# Retrieve track audio and image files

@bp.route('/play/<track_id>')
def play_track(track_id):
    track = Track.query.filter_by(id=track_id).first_or_404()
    return send_from_directory(app.config['SOUNDCLOUD_FOLDER'], track.path)


@bp.route('/image/<track_id>')
def download_image(track_id):
    track = Track.query.filter_by(id=track_id).first_or_404()
    return send_from_directory(app.config['SOUNDCLOUD_IMAGE_FOLDER'], track.image_path)


# # Artists
#
# @bp.route('/artists')
# def show_artists():
#     artists = Artist.query.order_by(Artist.created_at.desc())
#     artists, next_url, prev_url = paginate(artists)
#
#     return render_template('artists.html', title='Artists',
#                            artists=artists.items, next_url=next_url, prev_url=prev_url)
#
#
# @bp.route('/artist/<name>')
# def show_artist(name):
#     artist = Artist.query.filter_by(name=name).first_or_404()
#
#     albums = artist.albums
#     tracks = artist.tracks
#
#     return render_template('artist.html', title=artist.name,
#                            artist=artist, albums=albums, tracks=tracks)
#
#
# # Albums
#
# @bp.route('/albums')
# def show_albums():
#     albums = Album.query.order_by(Album.created_at.desc())
#     albums, next_url, prev_url = paginate(albums)
#
#     return render_template('albums.html', title='Albums',
#                            albums=albums.items, next_url=next_url, prev_url=prev_url)
#
#
# @bp.route('/album/<album_id>')
# def show_album(album_id):
#     album = Album.query.filter_by(id=album_id).first_or_404()
#     return render_template('album.html', title=album.name, album=album)
#
#
# # Tracks
#
# @bp.route('/tracks')
# def show_tracks():
#     tracks = Track.query.order_by(Track.created_at.desc())
#     tracks, next_url, prev_url = paginate(tracks)
#
#     return render_template('tracks.html', title='Tracks',
#                            tracks=tracks.items, next_url=next_url, prev_url=prev_url)
#
#
# @bp.route('/track/<track_id>')
# def show_track(track_id):
#     track = Track.query.filter_by(id=track_id).first_or_404()
#     return render_template('track.html', title=track.name, track=track)
#
#
# @bp.route('/play/<track_id>')
# def play_track(track_id):
#     track = Track.query.filter_by(id=track_id).first_or_404()
#     set_current_track(track)
#     return redirect(request.referrer or url_for('main.show_track', track_id=track_id))

