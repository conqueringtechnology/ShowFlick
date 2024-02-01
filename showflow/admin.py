from django.contrib import admin
from .models import Genre, Actor, Streaming, Watch


# Watch - the way it will show on admin.py
@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'display_genre', 'display_actor', 'display_streaming', 'release_year', 'rating', 'stars', 'length')


# Registering the following models to admin.py
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Streaming)


