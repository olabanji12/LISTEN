# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings
from requests import request, post
from django.contrib.auth import logout
from .utils import update_or_create_user_tokens, is_spotify_authenticated, get_user_tokens
import spotipy
from Dashboard.models import *
from Friends.models import UserPlaylist
from Friends.utils import generate_playlist_qrcode

def spotify_login(request):
    # Define your Spotify client credentials
    client_id = settings.SPOTIPY_CLIENT_ID
    client_secret = settings.SPOTIPY_CLIENT_SECRET
    redirect_uri = settings.SPOTIPY_REDIRECT_URI

    # Define the desired Spotify scopes as a space-separated string
    scope = 'user-read-private user-read-email playlist-modify-public user-top-read playlist-read-private'

    # Create the SpotifyOAuth object with credentials and scope
    sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)

    # Get the authorization URL with the scope
    auth_url = sp_oauth.get_authorize_url()
    # authenticated  = is_spotify_authenticated(request.session.session_key)
    return redirect(auth_url)

def get_user_display_name(request):
    user_tokens = get_user_tokens(request.session.session_key)
    sp = spotipy.Spotify(auth=user_tokens.access_token, requests_timeout=10, retries=10)
    user_info = sp.current_user()
    user_display_name = user_info["display_name"]

    return user_display_name

def get_user_display_id(request):
    user_tokens = get_user_tokens(request.session.session_key)
    sp = spotipy.Spotify(auth=user_tokens.access_token, requests_timeout=10, retries=10)
    user_info = sp.current_user()
    user_id = user_info["id"]

    return user_id

def get_user_dashboard_data(request):
    user_tokens = get_user_tokens(request.session.session_key)
    sp = spotipy.Spotify(auth=user_tokens.access_token, requests_timeout=100, retries=10)

    # get user_id
    
    user_id = get_user_display_id(request)

    # inserting user_id into UserProfile model
    UserProfileInstance = UserProfile(user_id = user_id)
    UserProfileInstance.save()

    # get user top 50 artist and album and image for artists and album
    top_artists = sp.current_user_top_artists(limit=50)
    top_tracks = sp.current_user_top_tracks(limit=50)
    artists_data = top_artists['items']
    tracks_data = top_tracks['items']
    
    # inserting user top 50 list in the model
    for counter, (artist, track) in enumerate(zip(artists_data,tracks_data), start=1):
        artist_name = artist['name']
        artist_image = artist['images'][1]['url']
        track_name = track['name']
        track_image = track['album']['images'][1]['url']
        UserTopArtistsInstance = UserTopArtists(user_id = UserProfileInstance, artist = artist_name, image = artist_image, rank = counter)
        UserTopArtistsInstance.save()
        UserTopTracksInstance = UserTopTracks(user_id = UserProfileInstance, track = track_name, image = track_image, rank = counter)
        UserTopTracksInstance.save()

def get_user_playlist(request):
    user_tokens = get_user_tokens(request.session.session_key)
    sp = spotipy.Spotify(auth=user_tokens.access_token, requests_timeout=100, retries=10)
    
    user_id = get_user_display_id(request)
    user_playlist = sp.current_user_playlists()
    
    for playlist in user_playlist['items']:
        playlist_name = playlist['name']
        playlist_url = playlist['external_urls']['spotify']
        generate_playlist_qrcode(request, playlist_url, user_id, playlist_name)
        playlist_image = playlist['images'][0]['url']
        if not UserPlaylist.objects.filter(user_id=user_id, name=playlist_name).exists():
            UserPlaylistInstance = UserPlaylist(user_id = user_id, name = playlist_name, image = playlist_image, url = playlist_url)
            UserPlaylistInstance.save()
    return HttpResponse("Playlist data saved successfully.")

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
    
    return redirect('user_dashboard')
    # Redirect the user to another page or perform further actions
    # return redirect('user_dashboard')

