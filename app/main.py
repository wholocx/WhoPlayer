from downloadserver import song_download_not_exist, song_search_on_server
from fastapi import FastAPI

# import requests 

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
def search_song(artist_name:str = "Ellie_Minibot", song_name:str = "Stupid heart"):
    result_id = song_search_on_server(song_name,artist_name)
    if result_id !=[]:
        return {"result_id": result_id}
    else:
        return{"result_id": "No song?"}

@app.get("/download_on_server")
def search_song(artist_name:str = "Ellie_Minibot", song_name:str = "never have i ever", yt_link:str = "https://www.youtube.com/watch?v=NE3x2wC3_Lw"):
    result_id = song_download_not_exist(song_name,artist_name,yt_link)
    if result_id != 0:
        return {"result_id": result_id}
    else:
        return{"result_id": "Song already exists"}