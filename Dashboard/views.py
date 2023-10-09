import spotipy
from django.shortcuts import render
from spotify_auth.utils import is_spotify_authenticated, get_user_tokens
from User.views import home
from spotify_auth.views import get_user_display_name, get_user_dashboard_data, get_user_display_id
from .forms import FilterNumberSelection
from .models import UserTopArtists, UserTopTracks, UserProfile
# Create your views here.
def user_dashboard(request):
    form = FilterNumberSelection(request.GET)
    is_authenticated  = is_spotify_authenticated(request.session.session_key)
    user_display_name = get_user_display_name(request)
    user_id = get_user_display_id(request)
    # get_user_dashboard_data(request)

    track_records = UserTopTracks.objects.filter(user_id = user_id).order_by('rank').all()
    artist_records = UserTopArtists.objects.filter(user_id = user_id).order_by('rank').all()

    artist_names = []
    artist_image_links = []
    track_names = []
    tracks_image_links = []

    for records in track_records:
        track_names.append(records.track)
        tracks_image_links.append(records.image)
    
    for records in artist_records:
        artist_names.append(records.artist)
        artist_image_links.append(records.image)

    if form.is_valid():
        number_filter = int(form.cleaned_data['number'])  # Get the selected number from the form

        # Filter your data based on the selected number
        artist_filtered_names = artist_names[:number_filter]
        artist_filtered_images = artist_image_links[:number_filter]

        track_filtered_names = track_names[:number_filter]
        track_filtered_images = tracks_image_links[:number_filter]

        artist_names_and_images = zip(artist_filtered_names,artist_filtered_images)
        tracks_names_and_images = zip(track_filtered_names,track_filtered_images)

        context = {
        'is_authenticated': is_authenticated,
        'artist_names_and_images':artist_names_and_images,
        'tracks_names_and_images':tracks_names_and_images,
        'user_display_name': user_display_name,
        'form': form,

        }

        # Render the template with the filtered data
        return render(request, "Dashboard/dashboard.html", context)
    
    artist_names_and_images = zip(artist_names,artist_image_links)
    tracks_names_and_images = zip(track_names,tracks_image_links)
    context = {
        'is_authenticated': is_authenticated,
        'artist_names_and_images':artist_names_and_images,
        'tracks_names_and_images':tracks_names_and_images,
        'user_display_name': user_display_name,
        'form': form,

    }
    return render(request,"Dashboard/dashboard.html", context)