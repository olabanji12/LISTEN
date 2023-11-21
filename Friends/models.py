from django.db import models

class UserPlaylist(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user_id', 'name')

class PlaylistQRCode(models.Model):
    url = models.URLField()
    user_id = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/')