from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from stdimage.utils import UploadToAutoSlugClassNameDir
from stdimage.models import StdImageField
from bands.models import Band


class UserManager(BaseUserManager):
    '''
    Manager for User.
    '''

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    '''
    Abstract User with unique email and no username.
    '''
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this'
                    ' admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_band_manager = models.BooleanField(
        _('band manager'),
        default=False,
        help_text=_(
            'Designates whether this user is a band manager '
            'and therefore can realize band actions.'
        ),
    )
    managed_band = models.OneToOneField(
        Band, null=True, blank=True, related_name='manager',
        on_delete=models.SET_NULL)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    avatar = StdImageField(_('avatar'), upload_to=UploadToAutoSlugClassNameDir(
        populate_from='username'), null=True)
    followed_bands = models.ManyToManyField(
        Band, verbose_name=_('Bands'), blank=True,
        related_name='followers')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_band_permission(self):
        """
        Returns a tuple with the managed band and a boolean whether user is
        a band manager or not.
        """
        return (self.managed_band, self.is_band_manager)
