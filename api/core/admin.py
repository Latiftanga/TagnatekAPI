from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models
from gradebook.models import AssignmentType, Subject


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email']

    fieldsets = (
        (_('Personal Info'), {'fields': ('email', 'role')}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser'
            )}),
        (_('Important dates'), {'fields': ('last_login',)})
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
            }),
        )


admin.site.register(models.School)
admin.site.register(Subject)
admin.site.register(AssignmentType)
admin.site.register(models.User, UserAdmin)
