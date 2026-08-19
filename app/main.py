from downloadserver import song_download_not_exist, song_search_on_server
from songlister import song_list_on_server
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

songs_on_server = song_list_on_server()

def update_songs_list():
    global songs_on_server
    songs_on_server = song_list_on_server()

@app.get("/")
def read_root():
    return {"found songs": song_list_on_server()}

@app.get("/search/")
def search_song(artist_name:str | None = None , song_name:str | None = None):
    result_id = song_search_on_server(song_name, artist_name)
    if result_id !=[]:
        return {"result_id": result_id}
    else:
        return{"result_id": "No song?"}

@app.get("/download_on_server/")
def search_song(artist_name:str , song_name:str, yt_link:str):
    result = song_download_not_exist(song_name,artist_name,yt_link)
    if result != 0:
        update_songs_list()
        return {"result": result}
    else:
        return{"result": "Song already exists"}
    
@app.get("/listening/{song_id}", response_class=FileResponse)
def send_song(song_id: int):
    for specific_song in song_list_on_server():
        if song_id == specific_song["id"]:
            print(specific_song["path_to_song"])
            return specific_song["path_to_song"]
