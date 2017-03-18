from rest_framework import serializers
from auth_ex.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    managed_band = serializers.HyperlinkedRelatedField(
        many=False, read_only=True,
        view_name='managed-band-detail')
    followed_bands = serializers.HyperlinkedRelatedField(
        many=True, read_only=True,
        view_name='followed-bands-detail')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name',
                  'last_name', 'avatar', 'managed_band',
                  'followed_bands',
                  'is_staff', 'is_band_manager', 'date_joined')
        lookup_field = 'username'
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
            'is_band_manager': {'read_only': True},
            'url': {'lookup_field': 'username'}
        }
