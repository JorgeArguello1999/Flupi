from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('api/', include('api.urls')),
    path('notify/', include('notify.urls')),
    path('login/', include('login.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
