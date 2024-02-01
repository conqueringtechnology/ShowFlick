import django_filters
from .models import Watch


# django filter
# search and filter for movies and shows
class WatchFilter(django_filters.FilterSet):

    class Meta:
        model = Watch
        fields = {
            'title': ['icontains'],
            'actor': ['exact'],
            'genre': ['exact'],
            'streaming': ['exact'],
            'release_year': ['exact'],
            'length': ['exact'],
            'stars': ['exact'],
            'rating': ['exact'],
            'watch_type': ['exact'],
        }
