from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from spotipy.oauth2 import SpotifyOAuth


# Create your views here.
def home(request):
    return render(request, 'User/home.html')

# def login_user(request):
#         if request.method == "POST":
#             username = request.POST['username']
#             password = request.POST['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request,user)
#                 return redirect('home')
#             else:
#                 messages.error(request, ("There Was An Error Logging In, Try Again..."))
#                 return redirect('login')
#         else:
#             return render(request, 'registration/login.html')

# def signup(request):
#     return render(request, 'registration/signup.html' )

# def spotify_login(request):
#     sp_oauth = SpotifyOAuth(request)
#     auth_url = sp_oauth.get_authorize_url()
#     return render(request, 'spotify_login.html', {'auth_url': auth_url})