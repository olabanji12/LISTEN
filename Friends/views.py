from django.shortcuts import render
from spotify_auth.views import get_user_playlist, get_user_display_id, get_user_display_name
from spotify_auth.utils import is_spotify_authenticated
from .models import UserPlaylist
# Create your views here.
def user_playlist(request):
    user_id = get_user_display_id(request)
    is_authenticated  = is_spotify_authenticated(request.session.session_key)
    user_display_name = get_user_display_name(request)
    get_user_playlist(request)

    playlist_records = UserPlaylist.objects.filter(user_id = user_id).all()

    playlist_names = []
    playlist_image = []
    playlist_url = []

    for records in playlist_records:
        playlist_names.append(records.name)
        playlist_image.append(records.image)
        playlist_url.append(records.url)
    
    playlist_name_image_links = zip(playlist_names, playlist_image, playlist_url)
    context = {
         'playlist_name_image_links': playlist_name_image_links,
         'is_authenticated': is_authenticated,
         'user_display_name': user_display_name,
     }
    return render(request, 'Friends/playlist.html', context)