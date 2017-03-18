
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from auth_ex.models import User

from .serilaizers import UserSerializer


class PermissionRenderer(BrowsableAPIRenderer):
    # Allow to watch create new user form
    # when user is not logged in

    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(
            data, accepted_media_type, renderer_context)
        context['display_edit_forms'] = True
        return context


class UserViewSet(viewsets.ModelViewSet):
    renderer_classes = (JSONRenderer, PermissionRenderer, )
    queryset = User.objects.all()
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
        return super(UserViewSet, self).get_permissions()
