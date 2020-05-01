from django.contrib import admin
from .models import Post


class Datecreated(admin.ModelAdmin):
    readonly_fields = ('datecreated',)


admin.site.register(Post, Datecreated)
