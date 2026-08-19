import flet as ft
import flet_audio as fta
import aiohttp
import os
import asyncio

# base_url = os.getenv("http://localhost:8081")
base_url = "http://localhost:8081"
download_path = "storage/songsaved/"

# local_songs = []
# implement saving local songs to the json file on every addition or deletion of the song

index = 0
state = ''
previous_id = 0
async def main(page: ft.Page):
    async def on_load_music():
        url = f"{base_url}/"
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()
    async def play_music(e: ft.ControlEventHandler[ft.ListTile]):         
            async def player(e: ft.ControlEventHandler[fta.Audio]):
                    global state
                    state = "playing"                
                    await e.control.play()
            global index
            global previous_id
            global state
            if previous_id == e.control.data["id"]:
                if state == "playing":
                    state = "paused"
                    await page.services[index].pause()
                elif state == "paused":
                    state = "playing"
                    await page.services[index].resume()
            elif previous_id == 0:   
                audio = fta.Audio(
                        autoplay = False,
                        src = f'{base_url}/listening/{e.control.data["id"]}',
                        on_loaded = player,
                        # on_state_change = pauser,
                        release_mode = fta.ReleaseMode.STOP)
                page.services.append(audio)
            elif previous_id != e.control.data["id"]:
                await page.services[index].release()
                audio = fta.Audio(
                    autoplay=False,
                    src = f'{base_url}/listening/{e.control.data["id"]}',
                    on_loaded= player,
                    release_mode=fta.ReleaseMode.STOP)
                page.services.append(audio)
                index = index + 1
            previous_id = e.control.data["id"]

    tiles = []


    async def tilemaker(music_list_main):
            for specific_song in music_list_main["found songs"]:
                song = ft.ListTile(
                    title = specific_song["song_name"],
                    subtitle = specific_song["artist_name"],
                    trailing=ft.PopupMenuButton(
                        icon = ft.Icons.MORE_VERT,
                        items= [ft.PopupMenuItem(content="Скачать"),
                                ft.PopupMenuItem(content="Удалить из кэша")]),
                    data = {
                        "artist_name": specific_song["artist_name"],
                        "id": specific_song["id"],
                        "path_to_song": specific_song["path_to_song"]
                    },
                    on_click= play_music)
                tiles.append(song)
            page.update()
            print("Page updated")

    SongListTiles = ft.ListView(
        controls = tiles, 
        expand=True, 
        scroll = ft.ScrollMode.HIDDEN, 
        spacing = 1,
        height = page.window.height-60,
        # padding = 10
        )

    def page_resize(e):
        SongListTiles.height=page.window.height-60
        SongListTiles.update()

    page.on_resize = page_resize

    def song_adder(new_song):
        tiles.append(ft.ListTile(
                    title = new_song["song_name"],
                    subtitle = new_song["artist_name"],
                    trailing=ft.PopupMenuButton(
                        icon = ft.Icons.MORE_VERT,
                        items= [ft.PopupMenuItem(content="Скачать"),
                                ft.PopupMenuItem(content="Удалить из кэша")]),
                    data = {
                        "artist_name": new_song["artist_name"],
                        "id": new_song["id"],
                        "path_to_song": new_song["path_to_song"]
                    },
                    on_click= play_music))
        SongListTiles.update()

    # Настройки страницы
    page.title = "Music Player"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    username = "wholock"    
    music_list_main = await on_load_music()
    await tilemaker(music_list_main)

    async def pauser(e: ft.Event[ft.Button]):
        global state
        if state == "playing":
            await page.services[0].pause()
            e.control.icon = ft.Icons.PLAY_CIRCLE
            state = "paused"
        elif state == "paused":
            await page.services[0].resume()
            state = "playing"
            e.control.icon = ft.Icons.PAUSE_CIRCLE
        page.update()

    async def drawer_clicked(e: ft.Event[ft.Button]):
        print("drawer_clicked")
        await handle_show_drawer()

    async def handle_show_drawer():
        print("handle_show_drawer")
        await page.show_drawer()

    def handle_dismissal(e: ft.Event[ft.NavigationDrawer]):
        print(f"Drawer dismissed!")

    async def handle_change(e: ft.Event[ft.NavigationDrawer]):
        print(f"Selected Index changed: {e.control.selected_index}")
        if(e.control.selected_index == 1):
            search_serv_clicked()
        await page.close_drawer()

    def search_clicked(e: ft.Event[ft.Button]):
        page.show_dialog(searcher)

    def search_closed(e: ft.Event[ft.Button]):
        song_name.value = ""
        singer_name.value = ""
        page.pop_dialog()

    def search_serv_clicked():
        page.show_dialog(searcher_on_server)

    async def search_song(e: ft.Event[ft.Button]):
        url = f"{base_url}/search"
        payload = {"artist_name": singer_name.value,"song_name": song_name.value}
        async with aiohttp.ClientSession() as session:
                async with session.get(url, params=payload) as response:
                    if response.status == 200:
                        song_name.value = ""
                        singer_name.value = ""
                        page.pop_dialog()
                        print(await response.json())
                        return await response.json()
                    else:
                        error_message = await response.text()
                        raise Exception(f"Ошибка: {error_message}")

    def popper(e: ft.Event[ft.Button]):
        page.pop_dialog()

    async def search_song_serv(e: ft.Event[ft.Button]):
        url = f"{base_url}/download_on_server"
        payload = {"artist_name": singer_name.value,"song_name": song_name.value, "yt_link": yt_link.value}
        async with aiohttp.ClientSession() as session:
                async with session.get(url, params=payload) as response:
                    if response.status == 200:
                        song_name.value = ""
                        singer_name.value = ""
                        yt_link.value = ""
                        page.pop_dialog()
                        new_song = await response.json()
                        return song_adder(new_song['result'])
                    else:
                        error_message = await response.text()
                        page.pop_dialog()
                        await asyncio.sleep(0.3)
                        page.show_dialog(ft.AlertDialog(
                                modal=False,        
                                title=ft.Text(f"Ошибка: Не удалось скачать песню. \nРезультат: {error_message}"),
                                on_dismiss= search_closed,
                                actions=[
                                    ft.ResponsiveRow(
                                        # run_spacing={ft.ResponsiveRowBreakpoint.XS: 10},
                                        controls=ft.Button(content="Ок", on_click= popper)),                 
                                    ],
                                actions_alignment=ft.MainAxisAlignment.END,
                                open=True))
                        song_name.value = ""
                        singer_name.value = ""
                        yt_link.value = ""
                        # raise Exception(f"Ошибка: {error_message}")

    bg_container = ft.Ref[ft.Container]()
    
    def handle_menu_click(e):
        color = e.control.content.value
        print(f"{color}.on_click")
        bg_container.current.content.value = f"{color} background color"
        bg_container.current.bgcolor = color.lower()
        page.update()

    song_name = ft.TextField(label="Введите название песни", autofocus=True)
    singer_name = ft.TextField(label="Введите исполнителя", autofocus=True)
    yt_link = ft.TextField(label="Введите ссылку на песню", autofocus=True)

    searcher = ft.AlertDialog(
        modal=False,        
        title=ft.Text("Поиск песни"),
        # content= [],
        actions=[
            ft.ResponsiveRow(
                run_spacing={ft.ResponsiveRowBreakpoint.XS: 10},
                controls=[
                    song_name,
                    singer_name,
                    ft.Button(content="Найти", on_click= search_song),
                    ft.Button(content = "Закрыть", on_click= search_closed)
                    ]),                 
            ],
        on_dismiss= search_closed,
        actions_alignment=ft.MainAxisAlignment.END,
        open=True)

    searcher_on_server = ft.AlertDialog(
        modal=False,        
        title=ft.Text("Поиск песни"),
        on_dismiss= search_closed,
        actions=[
            ft.ResponsiveRow(
                run_spacing={ft.ResponsiveRowBreakpoint.XS: 10},
                controls=[
                    song_name,  
                    singer_name,
                    yt_link,
                    ft.Button(content="Найти", on_click= search_song_serv),
                    ft.Button(content = "Закрыть", on_click= search_closed)
                    ]),                 
            ],
        actions_alignment=ft.MainAxisAlignment.END,
        open=True)

    menubar = ft.MenuBar(
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Режим прослушивания"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Онлайн"),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}
                        ),
                        on_click=handle_menu_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Сохраненные"),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN}
                        ),
                        on_click=handle_menu_click,

                    ),
                ],
            ),
        ],
    )

    page.drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.Container(height=12),
            ft.Text(f" {username}", size=25),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination( 
                label="Моя музыка",
                icon=ft.Icons.MUSIC_NOTE,
                selected_icon=ft.Icon(ft.Icons.MUSIC_NOTE),
                # on_click=
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.CLOUD_DOWNLOAD_OUTLINED,
                label="Скачать на сервер",
                selected_icon=ft.Icons.CLOUD_DOWNLOAD_OUTLINED,
                # on_click= 
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.AUDIO_FILE,
                label="Все медиа на сервере",
                selected_icon=ft.Icons.AUDIO_FILE,
                # on_click=
            ),
            ft.NavigationDrawerDestination(
                label="Настройки",
                icon=ft.Icons.SETTINGS,
                # on_click=
            ),
        ],
    )

    page.add(
        ft.SafeArea(
        ft.Column(controls = [
            ft.Row([            
                    ft.IconButton(
                    icon=ft.Icons.DEHAZE_OUTLINED,
                    style = ft.ButtonStyle(
                        icon_color=ft.Colors.WHITE,
                        icon_size=30
                    ),
                    tooltip="drawer button",
                    padding = 1,
                    on_click= drawer_clicked,),

                    menubar,
                    
                    ft.IconButton(
                    icon=ft.Icons.SEARCH,
                    style = ft.ButtonStyle(
                        alignment = ft.Alignment.CENTER,
                        icon_color=ft.Colors.WHITE,
                        icon_size=40),
                    tooltip="search button", 
                    padding = 1,             
                    on_click= search_clicked)]),
                    
            ft.Container(content = SongListTiles, 
            padding = 1),
            # ft.Row([
            # ft.IconButton(icon = ft.Icons.PAUSE_CIRCLE,
            #                 style = ft.ButtonStyle(
            #                 alignment = ft.Alignment.CENTER,
            #                 icon_color=ft.Colors.WHITE,
            #                 icon_size=40),
            #             tooltip="pause button",    
            #             on_click = pauser)]),
            ]),))
    page_resize(None)


    
if __name__ == "__main__":
    ft.run(main)