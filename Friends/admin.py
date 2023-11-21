from django.contrib import admin
from .models import UserPlaylist, PlaylistQRCode

# Register your models here.
admin.site.register(UserPlaylist)
admin.site.register(PlaylistQRCode)