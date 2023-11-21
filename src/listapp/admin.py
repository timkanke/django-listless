from django.contrib import admin

from .models import Image, Item


class imageAdmin(admin.ModelAdmin):
    list_display = ['title', 'photo']


admin.site.register(Image, imageAdmin)
