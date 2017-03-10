from django.db import models
from django.utils.translation import gettext_lazy as _
from stdimage.utils import UploadToAutoSlugClassNameDir
from stdimage.models import StdImageField


class Genre(models.Model):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Song(models.Model):
    title = models.CharField(_('title'), max_length=200)
    lyrics = models.TextField(_('lyrics'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('song')
        verbose_name_plural = _('songs')


class Album(models.Model):
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    image = StdImageField(_('image'), upload_to=UploadToAutoSlugClassNameDir(
        populate_from='title'), null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('album')
        verbose_name_plural = _('albums')


class Band(models.Model):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    image = StdImageField(_('image'), upload_to=UploadToAutoSlugClassNameDir(
        populate_from='name'), null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              related_name='band_genre',
                              verbose_name=_('genre'))
    albums = models.ForeignKey(Album, on_delete=models.CASCADE,
                               related_name='band_albums',
                               verbose_name=_('albums'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('band')
        verbose_name_plural = _('bands')
