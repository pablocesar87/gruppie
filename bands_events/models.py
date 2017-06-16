from django.db import models
from django.utils.translation import gettext_lazy as _
from stdimage.models import StdImageField
from stdimage.utils import UploadToAutoSlugClassNameDir

from bands.models import Band, Album


RELEASE = 'release'
TOUR = 'tour'
CONCERT = 'concert'
START_PROJECT = 'start_project'
MERCH = 'merch'
LINE_UP_CHANGE = 'line_up_change'

TYPE_EVENT = (
    (RELEASE, _('Release')),
    (TOUR, _('Tour')),
    (CONCERT, _('Concert')),
    (START_PROJECT, _('Start project')),
    (MERCH, _('Merchandising')),
    (LINE_UP_CHANGE, _('Line up change'))
)


class TourDates(models.Model):
    """
    This class will be used to be an inline for the list
    of dates that a tour has.
    """
    date = models.DateTimeField(_('Date of the event'), null=True)
    localization = models.CharField(
        _('Localization of the event'),
        help_text=_('Be as accurate as possible'),
        null=True
    )
    extra_info = models.TextField(
        _('Extra information for this date.'), blank=True)


class BandEvent(models.Model):
    name = models.CharField(_('Name of the event'))
    type_event = models.CharField(
        _('Type of event'), max_length=14, choices=TYPE_EVENT)
    band = models.ForeignKey(
        Band,
        verbose_name=_('Band'),
        related_name='events',
        on_delete=models.CASCADE
    )
    album = models.ForeignKey(
        Album,
        verbose_name=_('Album'),
        related_name='events',
        null=True,
        on_delete=models.SET_NULL
    )

    information = models.TextField(_('Information of the event'), blank=True)
    image = StdImageField(_('image'), upload_to=UploadToAutoSlugClassNameDir(
        populate_from='name'), null=True, blank=True)

    date = models.DateTimeField(_('Date of the event'), null=True)
    localization = models.CharField(
        _('Localization of the event'),
        help_text=_('Be as accurate as possible if it is a concert.'),
        null=True
    )

    tour_dates = models.ForeignKey(TourDates, blank=True)

    class Meta:
        verbose_name = _('Band Event')
        verbose_name_plural = _('Band Events')

    def __str__(self):
        return _('{}: {} {}'.format(
            self.type_event, self.name, self.band.__str__)
        )
