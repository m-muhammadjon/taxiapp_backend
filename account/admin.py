from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreateForm
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    list_display = ('email', 'fullname', 'phone_number', 'is_online', 'id')
    readonly_fields = ('id', 'date_joined')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'phone_number', 'password', 'password2',),
        }),
    )
