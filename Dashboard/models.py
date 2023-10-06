from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user_id = models.CharField(max_length=255, primary_key = True)
    # Add any additional user-related fields if needed

class UserTopArtists(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, to_field = 'user_id')
    artist = models.CharField(max_length=255)
    rank = models.PositiveIntegerField()

class UserTopAlbums(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, to_field = 'user_id')
    album = models.CharField(max_length=255)
    rank = models.PositiveIntegerField()
