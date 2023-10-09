from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user_id = models.CharField(max_length=255, primary_key = True)
    # Add any additional user-related fields if needed

class UserTopArtists(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, to_field = 'user_id')
    artist = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True)
    rank = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user_id', 'artist', 'image', 'rank')

class UserTopTracks(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, to_field = 'user_id')
    track = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True)
    rank = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user_id', 'track', 'image', 'rank')