from django.contrib import admin

from .models import Band, Album, Song, Genre


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    model = Band


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    model = Album


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    model = Song


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    model = Genre