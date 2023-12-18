from django.urls import path
from . import views

urlpatterns = [
    path("", views.notify_frontend, name="notify"),
    path("status/", views.notify_status, name="notify_status"),
    path("entry/<int:statuswork>", views.notify_backend, name="notify_entry"),
]