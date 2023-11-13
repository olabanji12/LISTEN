from django.db import models

class UserPlaylist(models.Model):
    user_id = models.CharField(max_length=255, primary_key = True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255)
