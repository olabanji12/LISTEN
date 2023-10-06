from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user_id = models.CharField(max_length=255, primary_key = True)
    # Add any additional user-related fields if needed

class Artist(models.Model):
    artist_name = models.CharField(max_length=255, primary_key = True)

class Album(models.Model):
    album_title = models.CharField(max_length=255, primary_key = True)

class UserTopArtists(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, to_field = 'user_id')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, to_field = 'artist_name')
    rank = models.PositiveIntegerField()

class UserTopAlbums(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, to_field = 'user_id')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, to_field = 'album_title')
    rank = models.PositiveIntegerField()
