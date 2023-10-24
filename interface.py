import flet as ft
from flet import *
import threading

# Modulo de utilidades netas
def start_utilities():
    import main

utilites = threading.Thread(target=start_utilities)
utilites.start()

def main(page: ft.Page):
    page.title = "Images Example"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 50

    img = ft.Image(
        src=f"./me/1.jpeg",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )
    images = ft.Row(expand=1, wrap=True, scroll="always")

    page.add(img, images)

    for i in range(0, 30):
        images.controls.append(
            ft.Image(
                src=f"./me/{i}.jpeg",
                width=200,
                height=200,
                fit=ft.ImageFit.NONE,
                border_radius=ft.border_radius.all(10),
            )
        )
    page.update()

utilites.join()

if __name__ == "__main__":
    # Lanzamos la APP para escritorio
    ft.app(target=main)
    # Lanzamos la APP para web 
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER)
