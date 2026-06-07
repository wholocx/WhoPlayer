import json
import yt_dlp


# Чтение списка песен
with open('AppBackend\DownloadServer\songlist.json', 'r') as f:
    song_data = json.load(f)

# Переводим словарь в строку, тк у нас пока только один объект в json
songs_on_server = song_data["songs_on_server"]

def song_search_on_server(input_song_name, artist_name_downloaded):
    found_id = []
    search__song_name = input_song_name.lower().replace(" ","")
    search_artist_name = artist_name_downloaded.lower().replace(" ","")
    search = search__song_name + search_artist_name
    for specific_song in songs_on_server:
        if (specific_song["song_name"].lower().replace(" ","") in search) or (specific_song["artist_name"].lower().replace(" ","") in search):
            found_id.append(specific_song["id"])
    return found_id


def song_download_not_exist(input_song_name,artist_name_downloaded, yt_link):
    print("Provide yt link to song:")
    download_link = yt_link
    search__song_name = input_song_name.lower().replace(" ","")
    search_artist_name = artist_name_downloaded.lower().replace(" ","")
    search = search__song_name + search_artist_name
    for specific_song in songs_on_server:
        if (specific_song["song_name"].lower().replace(" ","") not in search) or (specific_song["artist_name"].lower().replace(" ","") not in search):
            ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]}
            song_path = f'AppBackend\DownloadServer\SongFolder\{input_song_name}.%(ext)s'
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
            new_song_dict["path_to_song"] = "AppBackend\DownloadServer\SongFolder" + "/" + input_song_name + ".m4a"
            song_data["songs_on_server"].append(new_song_dict)
            with open('AppBackend\DownloadServer\songlist.json', 'w') as f:
                json.dump(song_data,f,indent=4)
            return(new_song_dict["id"])
        else:
            return(0)

