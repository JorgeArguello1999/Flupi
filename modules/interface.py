from kivy.lang import Builder
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.uix.video import Video
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.core.window import Window

# Modulos del sistema
import subprocess, signal

class MainApp(MDApp):
    title = "Hola Maxi"
    fonts = {
        "junegull": "./me/junegull.ttf"
    }
    Window.size = (1000, 750)

    def build(self):
        # Configuraciones principales
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        # Widget raíz
        root = FloatLayout()

        # Imagen de fondo
        background = Image(
            source="./me/fondo.png",
            allow_stretch=True,
            keep_ratio=False
        )

        # Mensaje
        layout = BoxLayout(
            orientation='vertical',
            spacing=10,
        )

        # Reproductor de video
        video_layout = BoxLayout(orientation='vertical', padding=95, spacing=10)
        player = Video(source="./me/video.mp4", size_hint=(1, None), height=250)
        player.state = "play"
        player.options = {"eos": "loop"}
        player.allow_fullscreen = True
        player.volume = 0
        video_layout.add_widget(player)

        # Botones
        buttons_layout = GridLayout(cols=2, spacing=10, size_hint=(1, None), height=50)
        exit_button = Button(text="Salir", on_release=self.exit_app)
        command_button = Button(text="Mostrar Comandos", on_release=self.show_commands)

        # Agregar elementos al diseño
        layout.add_widget(video_layout)
        layout.add_widget(buttons_layout)
        buttons_layout.add_widget(exit_button)
        buttons_layout.add_widget(command_button)

        # Agregar elementos al Layout
        root.add_widget(background)
        root.add_widget(layout)

        return root

    def exit_app(self, instance):
        App.get_running_app().stop()

    def show_commands(self, instance):
        content = Label(text="Comandos:\n1. Decir 'Hola Maxi' para saludar\n2. Botón 'Salir' para cerrar la aplicación", font_size='20sp')
        popup = Popup(title="Comandos", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == "__main__":
    MainApp().run()
