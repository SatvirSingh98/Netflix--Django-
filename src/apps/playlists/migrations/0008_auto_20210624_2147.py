# Generated by Django 3.2.4 on 2021-06-24 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0007_auto_20210623_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='order',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='playlist',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='playlists.playlist'),
        ),
    ]
