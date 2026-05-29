import flet as ft

def main(page: ft.Page):
    # Настройки страницы
    page.title = "Music Player"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    username = "wholock"    
    def handle_dismissal(e):
        print(f"Drawer dismissed!")

    def handle_change(e):
        print(f"Selected Index changed: {e.control.selected_index}")
        page.close(drawer)
    
    bg_container = ft.Ref[ft.Container]()
    
    def handle_menu_click(e):
        color = e.control.content.value
        print(f"{color}.on_click")
        bg_container.current.content.value = f"{color} background color"
        bg_container.current.bgcolor = color.lower()
        page.update()

    song_name = ft.TextField(label="Введите название песни")
    singer_name = ft.TextField(label="Введите исполнителя")
    searcher = ft.AlertDialog(
            open=True,
            modal=True,
            title=ft.Text("Поиск песни"),
            content=ft.Column([song_name], tight=True), #[singer_name],
            actions=[ft.Button(content="Найти", on_click= print("Поиск начат"))],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
        

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

    drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,controls=[
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
                icon=ft.Icon(ft.Icons.CLOUD_DOWNLOAD_OUTLINED),
                label="Скачать на сервер",
                selected_icon=ft.Icons.CLOUD_DOWNLOAD_OUTLINED,
                # on_click=
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.AUDIO_FILE),
                label="Все медиа на сервере",
                selected_icon=ft.Icons.AUDIO_FILE,
                # on_click=
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.SETTINGS),
                label="Настройки",
                selected_icon=ft.Icons.SETTINGS,
                # on_click=
            ),
        ],
    )

    page.add(
            ft.Row([            
                    ft.IconButton(
                    icon=ft.Icons.DEHAZE_OUTLINED,
                    icon_color=ft.Colors.WHITE,
                    icon_size=30,
                    tooltip="Yep",
                    on_click=lambda e: page.open(drawer),),
                    menubar,
                    
                    ft.IconButton(
                    alignment = ft.alignment.top_right,
                    icon=ft.Icons.SEARCH,
                    icon_color=ft.Colors.WHITE,
                    icon_size=40,
                    tooltip="Yep",                    
                    on_click= page.show_dialog(searcher),
                    )],
                ),
            # ft.SafeArea(content=searcher)        
        )

ft.app(target=main)