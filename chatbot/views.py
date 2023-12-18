from django.shortcuts import render
from .models import ImageProfile

# Create your views here.
def chatbot(request):
    imagen_perfil_bot = ImageProfile.objects.filter(name='bot').values()[0]['imagen']
    imagen_perfil_user = ImageProfile.objects.filter(name='user').values()[0]['imagen']

    return render(request, 'chatbot.html', {
        "imagen_ruta_bot": imagen_perfil_bot,
        "imagen_ruta_user": imagen_perfil_user
    })