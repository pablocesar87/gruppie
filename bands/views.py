
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from auth_ex.models import User
from .models import Band

from .serializers import UserSerializer, BandSerializer


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


class PermissionBandRenderer(BrowsableAPIRenderer):
    # Allow to watch create new user form
    # when user is not logged in

    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(
            data, accepted_media_type, renderer_context)
        request = renderer_context['request']
        if request.user.is_staff:
            context['display_edit_forms'] = True
        else:
            context['display_edit_forms'] = False
        return context


class UserViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, PermissionUserRenderer, )
    serializer_class = UserSerializer
    lookup_field = 'username'

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
    renderer_classes = (JSONRenderer, PermissionBandRenderer, )
    serializer_class = BandSerializer
    queryset = Band.objects.all()
    lookup_field = 'name'


    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'DELETE':
            self.permission_classes = (IsAdminUser,)
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()