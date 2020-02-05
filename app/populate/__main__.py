from app import app, db
from app.models import Track, Album, Artist

from app.scrape.util import get_tags

import os


SD_FOLDER = app.config['SOUNDCLOUD_FOLDER']
IMAGE_FOLDER = app.config['SOUNDCLOUD_IMAGE_FOLDER']


def create_new_track(path):

    # Get ID3 metadata on mp3 file
    full_path = os.path.join(SD_FOLDER, path)
    id3_tags = get_tags(full_path)

    title = id3_tags.get("title")  # Retrieve title from ID3
    artist_name = id3_tags.get("artist")  # Retrieve artist from ID3
    album_name = id3_tags.get("album")  # Retrieve album from ID3
    id3_genre = id3_tags.get("genre")  # Retrieve genre from ID3
    id3_release_date = id3_tags.get("date")  # Retrieve release date from ID3
    id3_cover = id3_tags.get("cover")  # Retrieve cover art image data from ID3

    # Construct track object
    track = Track.get_or_create(path=path)
    track.title = title

    # Set Artist and Album objects
    if artist_name is not None:
        artist = Artist.get_or_create(name=artist_name)
        track.artist = artist
    if album_name is not None:
        album = Album.get_or_create(name=album_name, artist_name=artist_name)
        track.album = album

    # Populate other ID3 columns
    track.genre = id3_genre
    track.release_date = id3_release_date

    # If ID3 contained cover art, create image file
    if id3_cover is not None:
        image_path = path.replace("/", " > ") + ".jpg"
        image_full_path = os.path.join(IMAGE_FOLDER, image_path)
        with open(image_full_path, 'wb') as f:
            f.write(id3_cover.data)

        track.image_path = image_path

    return track


def add_tracks_recur(folder=""):
    abs_folder = os.path.join(SD_FOLDER, folder)
    for name in os.listdir(abs_folder):
        abs_path = os.path.join(abs_folder, name)
        path = os.path.join(folder, name)
        if os.path.isdir(abs_path):
            add_tracks_recur(path)
        elif os.path.splitext(name)[1] == ".mp3":
            track = create_new_track(path)
            db.session.merge(track)
    db.session.commit()


def populate():
    add_tracks_recur()


if __name__ == '__main__':
    populate()
