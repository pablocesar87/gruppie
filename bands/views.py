
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, permissions, generics
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from rest_framework.reverse import reverse
from rest_framework.response import Response
from auth_ex.models import User
from .models import Band, Album, Song, Genre
from .serializers import (
    UserSerializer, BandSerializer,
    AlbumSerializer, GenreSerializer, SongSerializer,
    FollowBandSerializer
)


class ManagerBandPermission(permissions.BasePermission):
    message = _('You are not allowed to manage this band.')

    def has_object_permission(self, request, view, obj):
        managed_band, manager = request.user.get_band_permission()
        if obj.__class__ == Song:
            band = obj.album.band
        elif obj.__class__ == Album:
            band = obj.band
        else:
            band = obj
        return (band == managed_band and manager)


class PermissionUserRenderer(BrowsableAPIRenderer):
    # Allow to watch create new user form
    # when user is not logged in

    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(
            data, accepted_media_type, renderer_context)
        request = renderer_context['request']
        if request.user.is_authenticated():
            context['display_edit_forms'] = False
        else:
            context['display_edit_forms'] = True
        return context


class UserViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, PermissionUserRenderer, )
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def perform_update(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated,)
        if self.request.method == 'DELETE':
            self.permission_classes = (IsAdminUser, )
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class BandViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, PermissionUserRenderer, )
    serializer_class = BandSerializer
    queryset = Band.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'PUT':
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsAdminUser, ManagerBandPermission,)
        return super().get_permissions()


class AlbumViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, PermissionUserRenderer, )
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsAdminUser, ManagerBandPermission)
        return super().get_permissions()


class SongViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, PermissionUserRenderer, )
    serializer_class = SongSerializer
    queryset = Song.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsAdminUser, ManagerBandPermission)
        return super().get_permissions()


class GenreViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, PermissionUserRenderer, )
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()


class FolowBandViewSet(generics.UpdateAPIView):
    queryset = Band.objects.all()
    serializer_class = FollowBandSerializer
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Method for adding or removing band to the current user."""
        band = self.get_object()
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        if band in user.followed_bands.all():
            user.followed_bands.remove(band)
            user.save()
        else:
            user.followed_bands.add(band)
            user.save()
