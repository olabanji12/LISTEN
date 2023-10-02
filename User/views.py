from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from spotipy.oauth2 import SpotifyOAuth
from spotify_auth.views import get_user_display_name
from spotify_auth.utils import is_spotify_authenticated, get_user_tokens
import spotipy

# Create your views here.
def home(request):
    is_authenticated  = is_spotify_authenticated(request.session.session_key)
    
    if is_authenticated:
        user_display_name = get_user_display_name(request)
        context = {
            'is_authenticated': is_authenticated,
            'user_display_name': user_display_name,
        }
        return render(request, 'User/home.html', context)
    else:
        context = {
            'is_authenticated': is_authenticated,
        }
        return render(request, 'User/home.html', context)