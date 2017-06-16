from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(UserAdmin):
    add_form_template = 'auth_ex/user/add_form.html'

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'username',
                                         'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions',
                                       'is_band_manager')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Bands information'), {'fields': ('followed_bands',
                                             'managed_band')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',
                   'is_band_manager')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    list_filter = ('is_band_manager',)
    ordering = ('username',)

admin.site.register(User, UserAdmin)
