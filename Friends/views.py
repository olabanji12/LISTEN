from django.shortcuts import render
from spotify_auth.views import get_user_playlist
from spotify_auth.views import get_user_display_id
from .models import UserPlaylist
# Create your views here.
def user_playlist(request):
    user_id = get_user_display_id()
    get_user_playlist()

    playlist_records = UserPlaylist.objects.filter(user_id = user_id).all()

    playlist_names = []
    playlist_image = []
    playlist_url = []

    for records in playlist_records:
        playlist_names.append(records.name)
        playlist_image.append(records.image)
        playlist_url.append(records.url)
    
    context = {
         'playlist_names': playlist_names,
         'playlist_image': playlist_image,
         'playlist_url': playlist_url,
     }
    return render(request, 'playlist.html', context)