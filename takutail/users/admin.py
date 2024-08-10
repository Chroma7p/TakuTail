from django.contrib import admin
from .models import UserSake, UserWari, UserOther

@admin.register(UserSake)
class UserSakeAdmin(admin.ModelAdmin):
    list_display = ('user', 'sake', 'quantity')

@admin.register(UserWari)
class UserWariAdmin(admin.ModelAdmin):
    list_display = ('user', 'wari', 'quantity')

@admin.register(UserOther)
class UserOtherAdmin(admin.ModelAdmin):
    list_display = ('user', 'other', 'quantity')
