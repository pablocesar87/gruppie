
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from auth_ex.models import User
from .models import Band, Album, Song, Genre
from .serializers import (
    UserSerializer, BandSerializer,
    AlbumSerializer, GenreSerializer, SongSerializer
)


class PermissionUserRenderer(BrowsableAPIRenderer):
    # Allow to watch create new user form
    # when user is not logged in

    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(
            data, accepted_media_type, renderer_context)
        request = renderer_context['request']
        if request.user.is_authenticated():
            context['display_edit_forms'] = True
        else:
            context['display_edit_forms'] = False
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
        if self.request.method == 'POST' or self.request.method == 'DELETE':
            self.permission_classes = (IsAdminUser,)
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()


class AlbumViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, PermissionUserRenderer, )
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'DELETE':
            self.permission_classes = (IsAdminUser,)
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()


class SongViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, PermissionUserRenderer, )
    serializer_class = SongSerializer
    queryset = Song.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'DELETE':
            self.permission_classes = (IsAdminUser,)
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_band_manager:
            if request.user.managed_band == self.queryset.first().album.band:
                import pdb; pdb.set_trace()
                self.permission_classes = (IsAuthenticated,)
        return super().retrieve(request, *args, **kwargs)


class GenreViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, PermissionUserRenderer, )
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'DELETE':
            self.permission_classes = (IsAdminUser,)
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

