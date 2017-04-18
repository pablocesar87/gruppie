from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework import routers
from bands import views as bands_views

router = routers.DefaultRouter()
router.register(r'users', bands_views.UserViewSet, base_name='users')
router.register(r'bands', bands_views.BandViewSet, base_name='bands')
router.register(r'genres', bands_views.GenreViewSet, base_name='genres')
router.register(r'albums', bands_views.AlbumViewSet, base_name='albums')
router.register(r'songs', bands_views.SongViewSet, base_name='songs')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    url(r'^api/bands/(?P<pk>[0-9]+)/follow',
        bands_views.FolowBandViewSet.as_view(), name='follow')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^rosetta/', include('rosetta.urls')),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
