# Generated by Django 4.2.4 on 2023-10-06 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Dashboard", "0002_alter_usertopalbums_album_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserTopTracks",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("track", models.CharField(max_length=255)),
                ("rank", models.PositiveIntegerField()),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Dashboard.userprofile",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="UserTopAlbums",
        ),
    ]
