import json
import yt_dlp


# Чтение списка песен
with open('AppBackend\DownloadServer\songlist.json', 'r') as f:
    song_data = json.load(f)

# Переводим словарь в строку, тк у нас пока только один объект в json
songs_on_server = song_data["songs_on_server"]

def song_search_on_server():
    found_id = []
    input_name = input()
    search_name = input_name.lower().replace(" ","")
    
    for specific_song in songs_on_server:
        if search_name == specific_song["song_name"].lower().replace(" ",""):
            found_id.append(specific_song["id"])

    if found_id != []:
        print(f"song found, id is {found_id}")
        return found_id
    else:
        print("song not found((\nwant to download it? \n1-yes\n2-no")
        result = input()
        match result:
            case "1":
                return song_download_not_exist(input_name)
            case "2":
                pass
            case _:
                print("Unknown input. Stopping execution")


def song_download_not_exist(input_name):
    print("Provide yt link to song:")
    download_link = input()
    print("Please provide artist name")
    artist_name_downloaded = input()
    ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]}
    song_path = f'AppBackend\DownloadServer\SongFolder\{input_name}.%(ext)s'
    ydl_opts["outtmpl"] = song_path
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:        
        ydl.download(download_link)
    
    new_song_dict = {}
    last_id = songs_on_server[-1]["id"]
    new_id = last_id + 1
    new_song_dict["id"] = new_id
    new_song_dict["song_name"] = input_name
    new_song_dict["artist_name"] = artist_name_downloaded
    new_song_dict["download_link"] = download_link
    new_song_dict["path_to_song"] = "AppBackend\DownloadServer\SongFolder" + "/" + input_name + ".m4a"
    song_data["songs_on_server"].append(new_song_dict)
    with open('AppBackend\DownloadServer\songlist.json', 'w') as f:
        json.dump(song_data,f,indent=4)

song_search_on_server()
