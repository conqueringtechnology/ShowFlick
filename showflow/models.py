from django.db import models
from django.contrib.auth.models import User


# Define the model for the Actors table
class Actor(models.Model):
    first_name = models.CharField('First Name', blank=True, max_length=50)
    last_name = models.CharField('Last Name', blank=True, max_length=50)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


# Define the model for the movie or show Genre table
class Genre(models.Model):
    genre_name = models.CharField('Genre Name', max_length=50, blank=True)

    def __str__(self):
        return self.genre_name


# Define the model for the Streaming table
class Streaming(models.Model):
    name = models.CharField('Streaming App Name', blank=True, max_length=30)

    def __str__(self):
        return self.name


# Search to watch
class Watch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watches')
    title = models.CharField(max_length=50, help_text='Enter movie/show title.')
    actor = models.ManyToManyField(Actor, blank=True, help_text='Enter an actor.')
    genre = models.ManyToManyField(Genre, blank=True, help_text='Enter a genre.')
    streaming = models.ManyToManyField(Streaming, blank=True, help_text='Enter a streaming app name.')
    release_year = models.PositiveSmallIntegerField('Release Year', blank=True, null=True, help_text='Enter the movie/show release year')
    length = models.CharField('Movie/show Length', max_length=20, blank=True, null=True, help_text='Enter the length of the movie/show (e.g. 2h 20m)')
    stars = models.DecimalField('Movie/show Stars', max_digits=5, decimal_places=2, blank=True, null=True, help_text='Enter the number of stars.')
    url = models.URLField('URL', blank=True, null=True, help_text='Enter the movie/show URL.')
    description = models.TextField(max_length=1000, blank=True, help_text='Enter a brief description of the movie/show.')

    RATING_LIST = {
        ('G', 'G'),
        ('PG', 'PG'),
        ('PG-13', 'PG-13'),
        ('R', 'R'),
        ('NC-17', 'NC-17'),
        ('TV-Y', 'TV-Y'),
        ('TV-Y7', 'TV-Y7'),
        ('TV-Y FV', 'TV-Y FV'),
        ('TV-14', 'TV-14'),
        ('TV-MA', 'TV-MA'),
    }

    rating = models.CharField(
        'Movie/show Rating',
        max_length=10,
        choices=RATING_LIST,
        default='',
        blank=True,
        help_text='Select movie/show rating.')

    # Watch Type
    MOVIE_SHOW = (
        ('Movie', 'Movie'),
        ('Show', 'Show'),
    )

    watch_type = models.CharField(
        'Watch Type',
        max_length=10,
        choices=MOVIE_SHOW,
        default='MOVIE',
        blank=True,
        help_text='Select movie or show.',
    )

    def display_genre(self):
        return ', '.join(genre.genre_name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def display_actor(self):
        """Create a string for the Actor. This is required to display Actor in Admin."""
        return ', '.join(actor.last_name for actor in self.actor.all()[:3])

    display_actor.short_description = 'Actor'

    def display_streaming(self):
        """Create a string for the streaming. This is required to display streaming in Admin."""
        return ', '.join(streaming.name for streaming in self.streaming.all()[:3])

    display_streaming.short_description = 'streaming'

    def __str__(self):
        return self.title
