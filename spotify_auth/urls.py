from django.urls import path
from . import views

urlpatterns = [
    path('spotify_login/', views.spotify_login, name='spotify_login'),
    path('spotify_logout/', views.spotify_logout, name='spotify_logout'),
    path('callback/', views.spotify_callback, name='spotify_callback'),
    # path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
]
