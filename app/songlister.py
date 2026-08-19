import json


def song_list_on_server():
    with open('AppBackend/DownloadServer/songlist.json', 'r') as f:
        song_data = json.load(f)
    songs_on_server = song_data["songs_on_server"]
    found_songs = []
    for specific_song in songs_on_server:
        song_json = {}
        song_json["id"] = specific_song["id"]
        song_json["song_name"] = specific_song["song_name"]
        song_json["artist_name"] = specific_song["artist_name"]
        song_json["path_to_song"] = specific_song["path_to_song"]
        found_songs.append(song_json)
    return found_songs

