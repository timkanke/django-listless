from django.contrib import admin

from .models import File, Image, Item


class fileAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'file']


class imageAdmin(admin.ModelAdmin):
    list_display = ['title', 'photo']


class itemAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'publish']


admin.site.register(File, fileAdmin)
admin.site.register(Image, imageAdmin)
admin.site.register(Item, itemAdmin)
