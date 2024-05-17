from django.contrib import admin

from .models import Cat, File, Image, Item


class catAdmin(admin.ModelAdmin):
    list_display = ['name']


class fileAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'file']


class imageAdmin(admin.ModelAdmin):
    list_display = ['title', 'photo']


class itemAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'publish']


admin.site.register(Cat, catAdmin)
admin.site.register(File, fileAdmin)
admin.site.register(Image, imageAdmin)
admin.site.register(Item, itemAdmin)
