from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.uix.button import Button

class MultimediaApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Agrega un recuadro para reproducir imágenes
        self.image = Image(source='./me/1.jpeg')
        self.layout.add_widget(self.image)

        # Agrega un recuadro para reproducir videos
        self.video = Video(source='./me/video.mp4', state='play')
        self.layout.add_widget(self.video)

        # Agrega un botón para detener la reproducción
        self.stop_button = Button(text='Detener reproducción')
        self.stop_button.bind(on_press=self.stop_media)
        self.layout.add_widget(self.stop_button)

        return self.layout

    def stop_media(self, instance):
        # Detiene la reproducción de video
        self.video.state = 'stop'

        # Muestra un video específico
        self.video.source = './me/video.mp4'
        self.video.state = 'play'

if __name__ == '__main__':
    MultimediaApp().run()
