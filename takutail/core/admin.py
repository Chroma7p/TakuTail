from django.contrib import admin
from .models import Sake, Wari, Other

@admin.register(Sake)
class SakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'aroma', 'sweetness', 'bitterness', 'sourness', 'alcohol_content')

@admin.register(Wari)
class WariAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'aroma', 'sweetness', 'bitterness', 'sourness')

@admin.register(Other)
class OtherAdmin(admin.ModelAdmin):
    list_display = ('name', 'note')
