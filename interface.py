import flet as flt
import subprocess
import os 

modulo = "main.py"
# command = f"python3 {modulo}"
# Eliminaras hijito
command = f"python3 --version"

def main(page: flt.Page):
    page.title = "Hola maxi"
    page.theme_mode = flt.ThemeMode.DARK
    page.fonts = {
        "junegull": "./me/junegull.ttf"
    }
    page.theme = flt.Theme(font_family="junegull")

    # txt Bienvenida
    txt_bienvenida = flt.Text(
        value="¡Hola, soy Maxi!",
    )

    # JPG Maxi
    jpg_imagen = flt.Image(
        src="./me/2.jpeg"
    )

    stack_central = flt.Stack([
        flt.Container(width=50, height=50, bgcolor=flt.colors.YELLOW),
        flt.Container(width=25, height=25, bgcolor=flt.colors.BLACK),
        jpg_imagen
    ])

    # Añadimos los componentes
    page.add(
        flt.Row(
            controls=[txt_bienvenida]
        ),
        flt.Row(
            controls=[
                jpg_imagen
            ]
        ),
        stack_central
    )

    # Añadimos los cambios
    page.update()

if __name__ == "__main__":
    # Hilo a la escucha 
    maxi_process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Hilo principal
    flt.app(target=main)
