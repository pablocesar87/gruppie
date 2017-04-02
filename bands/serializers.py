from rest_framework import serializers
from auth_ex.models import User
from .models import Band, Genre, Song, Album


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """User Serializer."""

    managed_band = serializers.HyperlinkedRelatedField(
        many=False, read_only=True,
        view_name='bands-detail',
    )
    followed_bands = serializers.HyperlinkedRelatedField(
        many=True, read_only=True,
        view_name='bands-detail'
    )

    class Meta:
        """Meta class User Serializer."""

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
        }


class BandSerializer(serializers.HyperlinkedModelSerializer):
    """Band Serializer."""

    genre = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='genres-detail')

    albums = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='albums-detail')

    managed_by = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='users-detail',
        source='manager')

    class Meta:
        """Meta class Band Serializer."""

        model = Band
        fields = ('id', 'name', 'description', 'image',
                  'genre', 'albums', 'managed_by')


class GenreSerializer(serializers.ModelSerializer):
    """Genre Serializer."""

    bands = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='bands-detail',
        source='bands_in_genre'
    )

    class Meta:
        """Genre Serializer."""

        model = Genre
        fields = ('id', 'name', 'description', 'bands')


class SongSerializer(serializers.HyperlinkedModelSerializer):
    """Song Serializer."""

    band = serializers.SerializerMethodField()
    album = serializers.HyperlinkedRelatedField(
        view_name='albums-detail', read_only=True)

    class Meta:
        """Meta class Song Serializer."""

        model = Song
        fields = ('id', 'title', 'lyrics', 'length', 'album',
                  'band')

    def get_band(self, obj):
        """Return the serializable name of the album band."""
        return obj.album.band.serializable_value('name')


class AlbumSerializer(serializers.ModelSerializer):
    """Album Serializer."""

    songs = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='songs-detail')

    band = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bands-detail')

    class Meta:
        """Meta class Album Serializer."""

        model = Album
        fields = ('id', 'title', 'description', 'image',
                  'songs', 'band')
