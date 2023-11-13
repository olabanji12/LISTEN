from django.urls import path
from . import views

urlpatterns =[
    path('', views.user_playlist, name = "user_playlist")
]