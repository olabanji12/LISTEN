# Create your views here.
from django.shortcuts import redirect, render
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings
from requests import Request, post

def spotify_login(request):
    # Define your Spotify client credentials
    client_id = settings.SPOTIPY_CLIENT_ID
    client_secret = settings.SPOTIPY_CLIENT_SECRET
    redirect_uri = settings.SPOTIPY_REDIRECT_URI

    # Define the desired Spotify scopes as a space-separated string
    scope = 'user-read-private user-read-email playlist-modify-public'

    # Create the SpotifyOAuth object with credentials and scope
    sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)

    # Get the authorization URL with the scope
    auth_url = sp_oauth.get_authorize_url()
    
    return redirect(auth_url)

def spotify_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')

    # This request the acess token requied to interact with the api
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
    print("Access Token:", token_type)
    
    # sp_oauth = SpotifyOAuth(request)
    # code = request.GET.get('code')
    # token_info = sp_oauth.get_access_token(code)

    # # Store the Spotify access token in the user session or database
    # request.session['spotify_token'] = token_info

    # Redirect the user to another page or perform further actions
    return render(request, 'spotify_auth/callback_success.html')
# '/spotify_callback.html'
