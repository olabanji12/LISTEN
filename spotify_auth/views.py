# Create your views here.
from django.shortcuts import redirect, render
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings
from requests import request, post
from django.contrib.auth import logout
from .utils import update_or_create_user_tokens, is_spotify_authenticated, get_user_tokens
import spotipy
from django.http import HttpRequest


def spotify_login(request):
    # Define your Spotify client credentials
    client_id = settings.SPOTIPY_CLIENT_ID
    client_secret = settings.SPOTIPY_CLIENT_SECRET
    redirect_uri = settings.SPOTIPY_REDIRECT_URI

    # Define the desired Spotify scopes as a space-separated string
    scope = 'user-read-private user-read-email playlist-modify-public user-top-read'

    # Create the SpotifyOAuth object with credentials and scope
    sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)

    # Get the authorization URL with the scope
    auth_url = sp_oauth.get_authorize_url()
    # authenticated  = is_spotify_authenticated(request.session.session_key)
    return redirect(auth_url)

def get_user_display_name(request):
    user_tokens = get_user_tokens(request.session.session_key)
    sp = spotipy.Spotify(user_tokens.access_token)
    user_info = sp.current_user()
    user_display_name = user_info["display_name"]

    return user_display_name

def spotify_logout(request): 
    logout(request)  # Logs out the user
    return redirect('home')
  
def spotify_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')

    # This request the access token requied to interact with the api
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIPY_REDIRECT_URI,
        'client_id': settings.SPOTIPY_CLIENT_ID,
        'client_secret': settings.SPOTIPY_CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    if not request.session.exists(request.session.session_key):
        request.session.create()
    
    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)
    
    is_authenticated  = is_spotify_authenticated(request.session.session_key)
    # Redirect the user to another page or perform further actions
    return redirect('user_dashboard')

