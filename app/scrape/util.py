from mutagen.mp3 import MP3, EasyMP3
from mutagen.id3 import APIC, WXXX
from mutagen.id3 import ID3 as OldID3

import requests, os
import re


# File Utility


def mkdir_if_not_exists(fp):
    if not os.path.exists(fp):
        os.mkdir(fp)


def sanitize_filename(filename):
    """
    Make sure filenames are valid paths.
    """
    sanitized_filename = re.sub(r'[/\\:*?"<>|]', '-', filename)
    # sanitized_filename = sanitized_filename.replace('&', 'and')
    sanitized_filename = sanitized_filename.replace('"', '')
    sanitized_filename = sanitized_filename.replace("'", '')
    sanitized_filename = sanitized_filename.replace("/", '')
    sanitized_filename = sanitized_filename.replace("\\", '')

    if sanitized_filename[0] == '.':
        sanitized_filename = u'dot' + sanitized_filename[1:]

    return sanitized_filename


def tag_file(filename, artist, title, date=None, genre=None, artwork_url=None, album=None, track_number=None, url=None):
    """
    Attempt to put ID3 tags on an mp3 file.
    Args:
        artist (str):
        title (str):
        date (int):
        genre (str):
        artwork_url (str):
        album (str):
        track_number (str):
        filename (str):
        url (str):
    """

    try:
        audio = EasyMP3(filename)
        audio.tags = None
        audio["artist"] = artist
        audio["title"] = title
        if date:
            audio["date"] = date
        if album:
            audio["album"] = album
        if track_number:
            audio["tracknumber"] = track_number
        if genre:
            audio["genre"] = genre
        if url:  # saves the tag as WOAR
            audio["website"] = url
        audio.save()

        if artwork_url:

            artwork_url = artwork_url.replace('https', 'http')

            mime = 'image/jpeg'
            if '.jpg' in artwork_url:
                mime = 'image/jpeg'
            if '.png' in artwork_url:
                mime = 'image/png'

            if '-large' in artwork_url:
                new_artwork_url = artwork_url.replace('-large', '-t500x500')
                try:
                    image_data = requests.get(new_artwork_url).content
                except Exception as e:
                    # No very large image available.
                    image_data = requests.get(artwork_url).content
            else:
                image_data = requests.get(artwork_url).content

            audio = MP3(filename, ID3=OldID3)
            audio.tags.add(
                APIC(
                    encoding=3,  # 3 is for utf-8
                    mime=mime,
                    type=3,  # 3 is for the cover image
                    desc='Cover',
                    data=image_data
                )
            )
            audio.save()

        # because there is software that doesn't seem to use WOAR we save url tag again as WXXX
        if url:
            audio = MP3(filename, ID3=OldID3)
            audio.tags.add(WXXX(encoding=3, url=url))
            audio.save()

        return True

    except Exception as e:
        return False


def get_tags(filename):
    tags = {}

    easy = EasyMP3(filename)
    for k, v in easy.tags.items():
        tags[k] = v[0]

    hard = MP3(filename, ID3=OldID3)
    cover = hard.tags.get("APIC:Cover")
    if cover is not None:
        tags["cover"] = cover

    return tags

