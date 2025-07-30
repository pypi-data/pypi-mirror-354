import re

import auto_dlp.downloader as downloader
import auto_dlp.file_locations as fs
from auto_dlp import playlist_items
from auto_dlp.name_cleaning import clean_name


# Yields: song name, song id, artist and file getter (a method)
def _iter_songs(config, artist=None):
    if artist is None:
        for artist in config.artists:
            yield from _iter_songs(config, artist)

    for name, song_id in artist.songs.items():
        yield name, song_id, artist.name, lambda: fs.try_get_song_file(artist.name, name)

    for playlist_name, playlist_id in artist.playlists.items():
        for entry in playlist_items.get(config, playlist_id):
            name = clean_name(config, entry["name"])
            song_id = entry["id"]

            yield (name, song_id, artist.name,
                   lambda: fs.try_get_song_file(artist.name, name, playlist_name))


# Yields: song name, song id, song file and item getter (a method)
def _get_playlist_items(config, artist):
    for entry in playlist_items.get(config, playlist_id):
        song_name = clean_name(config, entry["name"])
        song_id = entry["id"]

        song_file = fs.try_get_song_file(artist, song_id, playlist_name)
        if song_file is None: continue

        yield song_name, song_id, song_file


# Yields: playlist name, playlist id and artist
def _iter_playlists(config, artist=None):
    if artist is None:
        for artist in config.artists:
            yield from _iter_playlists(config, artist)

    for playlist_name, playlist_id in artist.playlists.items():
        yield (playlist_name, playlist_id, artist.name,
               lambda: _get_playlist_items(config, artist))


def _delete_song_file(song_name, song_id, artist, file):
    return
    print(f"Deleting song {song_name} ({song_id}) by {artist}: {file}")
    file_getter.unlink(missing_ok=True)
    downloader.delete_cached_version(song_id)


def _delete_playlist(playlist_name, playlist_id, artist, item_getter):
    print(f"Deleting playlist {playlist_name} ({playlist_id}) by {artist}:")
    for playlist_name, playlist_id in artist.playlists.items():
        for song_name, song_id, song_file in item_getter():
            _delete_song_file(song_name, song_id, artist, song_file)


# Yields: object type, object name, object id, artist and object deleter (method)
def _get_obj_locations(config, obj_id):
    obj_re = re.compile(obj_id, flags=re.IGNORECASE)

    for song_name, song_id, artist, file_getter in _iter_songs(config):
        if song_id == obj_id or obj_re.fullmatch(song_name) is not None:
            yield ("song", song_name, song_id, artist,
                   lambda: _delete_song_file(song_name, song_id, artist, file_getter()))

    for playlist_name, playlist_id, artist, item_getter in _iter_playlists(config):
        if playlist_id == obj_id or obj_re.fullmatch(playlist_name) is not None:
            yield ("playlist", playlist_name, playlist_id, artist,
                   lambda: _delete_playlist(playlist_name, playlist_id, artist, item_getter))


def redownload(config, obj):
    matches = list(_get_obj_locations(config, obj))
    print(f"Found the following matches for {obj}:")
    for obj_type, obj_name, obj_id, artist, _ in matches:
        print(f"Found {obj_type} {obj_name} ({obj_id}) by {artist}")

    confirmation = input(f"Really redownload all matches for {obj}? (y/n) ")
    if confirmation.strip() != "y":
        print("Aborted")
        return

    for _, _, _, _, deleter in matches:
        deleter()
