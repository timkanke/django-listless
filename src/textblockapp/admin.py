from django.contrib import admin

from .models import Text


class textAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title']


admin.site.register(Text, textAdmin)
