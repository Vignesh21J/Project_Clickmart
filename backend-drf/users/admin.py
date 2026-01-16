from django.contrib import admin
from .models import User

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
# admin.site.register(User)


class UserAdmin(BaseUserAdmin):
    list_display = ['email','first_name','last_name','is_staff','is_active']
    fieldsets = ()

admin.site.register(User, UserAdmin)
