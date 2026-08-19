import json
import yt_dlp


# Чтение списка песен
with open('AppBackend/DownloadServer/songlist.json', 'r') as f:
    song_data = json.load(f)

# Переводим словарь в строку, тк у нас пока только один объект в json
songs_on_server = song_data["songs_on_server"]

def song_search_on_server(input_song_name, artist_name_downloaded):
    print("search started")
    found_id = []
    search_song_name = input_song_name.lower().replace(" ","")
    search_artist_name = artist_name_downloaded.lower().replace(" ","")
    for specific_song in songs_on_server:
        specific_song_searchable_name = specific_song["song_name"].lower().replace(" ","")
        specific_artist_searchable_name = specific_song["artist_name"].lower().replace(" ","")
        if ((not search_song_name or search_song_name in specific_song_searchable_name) 
            and 
            (not search_artist_name or search_artist_name in specific_artist_searchable_name)):
            found_id.append(specific_song["id"])
    return found_id


def song_download_not_exist(input_song_name,artist_name_downloaded, yt_link):
    print("Provide yt link to song:")
    download_link = yt_link
    search_song_name = input_song_name.lower().replace(" ","")
    search_artist_name = artist_name_downloaded.lower().replace(" ","")
    for specific_song in songs_on_server:
        specific_song_searchable_name = specific_song["song_name"].lower().replace(" ","")
        specific_artist_searchable_name = specific_song["artist_name"].lower().replace(" ","")
        if (not(not search_song_name or search_song_name in specific_song_searchable_name) 
            and 
            not(not search_artist_name or search_artist_name in specific_artist_searchable_name)):
            ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]}
            song_path = f'AppBackend/DownloadServer/SongFolder/{input_song_name}.%(ext)s'
            ydl_opts["outtmpl"] = song_path
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:        
                ydl.download(download_link)
            
            new_song_dict = {}
            last_id = songs_on_server[-1]["id"]
            new_id = last_id + 1
            new_song_dict["id"] = new_id
            new_song_dict["song_name"] = input_song_name
            new_song_dict["artist_name"] = artist_name_downloaded
            new_song_dict["download_link"] = download_link
            new_song_dict["path_to_song"] = "AppBackend/DownloadServer/SongFolder/" + input_song_name + f".m4a"
            song_data["songs_on_server"].append(new_song_dict)
            with open('AppBackend/DownloadServer/songlist.json', 'w') as f:
                json.dump(song_data,f,indent=4)
            song_json = {}
            song_json["id"] = new_id
            song_json["song_name"] = input_song_name
            song_json["artist_name"] = artist_name_downloaded
            song_json["path_to_song"] = new_song_dict["path_to_song"]
            print(song_json)
            return(song_json)
        else:
            return(0)

