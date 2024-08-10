from django.contrib import admin
from .models import UserSake, UserWari, UserOther

from django.contrib import admin
from .models import UserSake, UserWari, UserOther

class UserSakeAdmin(admin.ModelAdmin):
    list_display = ('user', 'sake', 'owned')

class UserWariAdmin(admin.ModelAdmin):
    list_display = ('user', 'wari', 'owned')

class UserOtherAdmin(admin.ModelAdmin):
    list_display = ('user', 'other', 'owned')

