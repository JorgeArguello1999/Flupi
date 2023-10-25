from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.video import Video
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.app import App

class MainApp(MDApp):
    title = "Hola Maxi"
    def build(self):
        # Configuraciones principales
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        # Mensaje
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Texto de bienvenida
        welcome_label = Label(text="Hola, bienvenido, soy Maxi", font_size='30sp', halign='center', valign='middle')
        
        # Reproductor de video
        player = Video(source="./me/video.mp4")
        player.state = "play"
        player.options = {"eos": "loop"}
        player.allow_fullscreen = True

        # Texto para saludar
        greet_label = Label(text="Di, hola Maxi", font_size='30sp', halign='center', valign='middle')

        # Botones
        buttons_layout = GridLayout(cols=2, spacing=10, size_hint=(1, None), height=50)
        exit_button = Button(text="Salir", on_release=self.exit_app)
        command_button = Button(text="Mostrar Comandos", on_release=self.show_commands)

        # Agregar elementos al diseño
        layout.add_widget(welcome_label)
        layout.add_widget(player)
        layout.add_widget(greet_label)
        layout.add_widget(buttons_layout)
        buttons_layout.add_widget(exit_button)
        buttons_layout.add_widget(command_button)

        return layout

    def exit_app(self, instance):
        App.get_running_app().stop()

    def show_commands(self, instance):
        content = Label(text="Comandos:\n1. Decir 'Hola Maxi' para saludar\n2. Botón 'Salir' para cerrar la aplicación", font_size='20sp')
        popup = Popup(title="Comandos", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == "__main__":
    MainApp().run()