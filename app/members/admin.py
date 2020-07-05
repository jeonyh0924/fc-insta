from django.contrib import admin
from django.contrib.auth import get_user_model

from members.models import Profile

User = get_user_model()


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'email']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'username', 'introduce']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
