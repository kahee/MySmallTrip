from django.contrib import admin

from .models import User

# Register your models here.

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'img_profile')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.register(User, UserAdmin)
