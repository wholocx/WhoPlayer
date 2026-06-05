import flet as ft

def main(page: ft.Page):
    # Настройки страницы
    page.title = "Music Player"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    username = "wholock"    

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

    def search_song(e: ft.Event[ft.Button]):
        # накатать штуку для передачи инфы на апи
        print(song_name.value, singer_name.value)
        song_name.value = ""
        singer_name.value = ""
        # return (song_name, singer_name)
        print(song_name.value, singer_name.value)
        page.pop_dialog()
        # page.show_dialog()

    def search_song_serv(e: ft.Event[ft.Button]):
        print(song_name.value, singer_name.value)
        song_name.value = ""
        singer_name.value = ""
        page.pop_dialog()

    bg_container = ft.Ref[ft.Container]()
    
    def handle_menu_click(e):
        color = e.control.content.value
        print(f"{color}.on_click")
        bg_container.current.content.value = f"{color} background color"
        bg_container.current.bgcolor = color.lower()
        page.update()

    song_name = ft.TextField(label="Введите название песни", autofocus=True)
    singer_name = ft.TextField(label="Введите исполнителя", autofocus=True)

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
            ft.Row([            
                    ft.IconButton(
                    icon=ft.Icons.DEHAZE_OUTLINED,
                    style = ft.ButtonStyle(
                        icon_color=ft.Colors.WHITE,
                        icon_size=30
                    ),
                    tooltip="drawer button",
                    on_click= drawer_clicked,),

                    menubar,
                    
                    ft.IconButton(
                    icon=ft.Icons.SEARCH,
                    style = ft.ButtonStyle(
                        alignment = ft.Alignment.CENTER,
                        icon_color=ft.Colors.WHITE,
                        icon_size=40,
                    ),
                    tooltip="search button",              
                    on_click= search_clicked,
                    )
                    ],),
            # ft.SafeArea(content=searcher)        
        )

if __name__ == "__main__":
    ft.run(main)