import spotipy
from django.shortcuts import render
from spotify_auth.utils import is_spotify_authenticated, get_user_tokens

# Create your views here.
def user_dashboard(request):
    is_authenticated  = is_spotify_authenticated(request.session.session_key)
    print(is_authenticated)
    user_tokens = get_user_tokens(request.session.session_key)
    
    sp =spotipy.Spotify(user_tokens.access_token)
    top_artists = sp.current_user_top_artists(limit=10)
    top_tracks = sp.current_user_top_tracks(limit=10)
    artists_data = top_artists['items']
    tracks_data = top_tracks['items']


    artist_names = []
    artist_image_links = []
    track_names = []
    tracks_image_links = []

    for artist in artists_data:
        artist_names.append(artist["name"])
        artist_image_links.append(artist['images'][1]['url'])


    for tracks in tracks_data:
        track_names.append(tracks['name'])
        tracks_image_links.append(tracks['album']['images'][1]['url'])
        
   
    artist_names_and_images = zip(artist_names,artist_image_links)
    tracks_names_and_images = zip(track_names,tracks_image_links)
    context = {
        'artist_names': artist_names,
        'track_names': track_names,
        'is_authenticated': is_authenticated,
        'artist_image_links': artist_image_links,
        'tracks_image_links': tracks_image_links,
        'artist_names_and_images':artist_names_and_images,
        'tracks_names_and_images':tracks_names_and_images,
    }
    return render(request,"Dashboard/dashboard.html", context)