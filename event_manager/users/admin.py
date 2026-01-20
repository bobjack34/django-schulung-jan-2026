"""Um ein neues User-Model in der Admin zu bearbeiten,
muss eine eigene User-Admin angelegt werden."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    pass
