from django.db import models
from django.utils.translation import gettext_lazy as _
from stdimage.utils import UploadToAutoSlugClassNameDir
from stdimage.models import StdImageField
from django.core.urlresolvers import reverse


class Genre(models.Model):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Band(models.Model):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    image = StdImageField(_('image'), upload_to=UploadToAutoSlugClassNameDir(
        populate_from='name'), null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              related_name='bands_in_genre',
                              verbose_name=_('genre'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('band')
        verbose_name_plural = _('bands')


class Album(models.Model):
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    image = StdImageField(_('image'), upload_to=UploadToAutoSlugClassNameDir(
        populate_from='title'), null=True, blank=True)
    band = models.ForeignKey(Band, on_delete=models.CASCADE,
                             related_name='albums',
                             verbose_name=_('band'), null=True, blank=True)

    def __str__(self):
        return self.title

    def get_album_length(self):
        # TODO: Sum of the songs lengths
        pass

    class Meta:
        verbose_name = _('album')
        verbose_name_plural = _('albums')


class Song(models.Model):
    title = models.CharField(_('title'), max_length=200)
    lyrics = models.TextField(_('lyrics'), blank=True)
    length = models.TimeField(_('song length'), null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE,
                              related_name='songs',
                              verbose_name=_('album'), null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('song')
        verbose_name_plural = _('songs')
