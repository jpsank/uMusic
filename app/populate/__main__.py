from app import app, db
from app.models import Track, Album, Artist

from app.scrape.util import get_tags

import os, json


SD_FOLDER = app.config['SOUNDCLOUD_FOLDER']
IMAGE_FOLDER = app.config['SOUNDCLOUD_IMAGE_FOLDER']


def create_new_track(name, artist_name=None, album_name=None):
    artist = None
    album = None
    path = ''
    # If has artist, add artist folder to the path and create artist object
    if artist_name is not None:
        path = os.path.join(path, artist_name)

        artist = Artist.get_or_create(name=artist_name)
    # If in album, add album folder to the path and create album object
    if album_name is not None:
        path = os.path.join(path, album_name)

        album = Album.get_or_create(name=album_name)
    # Add mp3 file to the path
    path = os.path.join(path, name)

    # Get ID3 metadata on mp3 file
    full_path = os.path.join(SD_FOLDER, path)
    id3_tags = get_tags(full_path)

    id3_genre = id3_tags.get("genre")  # Retrieve genre from ID3
    id3_title = id3_tags.get("title")  # Retrieve title from ID3
    id3_release_date = id3_tags.get("date")  # Retrieve release date from ID3
    id3_cover = id3_tags.get("cover")  # Retrieve cover art image data from ID3

    # Construct track object
    track = Track.get_or_create(name=name, path=path)
    if artist is not None:
        track.artist = artist
    if album is not None:
        album.artist = artist
        track.album = album

    # Populate ID3 columns
    track.id3_genre = id3_genre
    track.id3_title = id3_title
    track.id3_release_date = id3_release_date

    # If ID3 contained cover art, create image file
    if id3_cover is not None:
        image_path = path.replace("/", " > ") + ".jpg"
        image_full_path = os.path.join(IMAGE_FOLDER, image_path)
        with open(image_full_path, 'wb') as f:
            f.write(id3_cover.data)

        track.image_path = image_path

    return track


def add_tracks_recur(folder, sub_folders=()):
    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        if os.path.isdir(path):
            add_tracks_recur(path, sub_folders=[*sub_folders, name])
        elif os.path.splitext(name)[1] == ".mp3":
            track = create_new_track(name, *sub_folders)
            db.session.merge(track)
    db.session.commit()


if __name__ == '__main__':
    add_tracks_recur(SD_FOLDER)
