# Generated by Django 4.1.1 on 2024-02-01 03:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='Last Name')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(blank=True, max_length=50, verbose_name='Genre Name')),
            ],
        ),
        migrations.CreateModel(
            name='Streaming',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, verbose_name='Streaming App Name')),
            ],
        ),
        migrations.CreateModel(
            name='Watch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter movie/show title.', max_length=50)),
                ('release_year', models.PositiveSmallIntegerField(blank=True, help_text='Enter the movie/show release year', null=True, verbose_name='Release Year')),
                ('length', models.CharField(blank=True, help_text='Enter the length of the movie/show (e.g. 2h 20m)', max_length=20, null=True, verbose_name='Movie/show Length')),
                ('stars', models.DecimalField(blank=True, decimal_places=2, help_text='Enter the number of stars.', max_digits=5, null=True, verbose_name='Movie/show Stars')),
                ('url', models.URLField(blank=True, help_text='Enter the movie/show URL.', null=True, verbose_name='URL')),
                ('description', models.TextField(blank=True, help_text='Enter a brief description of the movie/show.', max_length=1000)),
                ('rating', models.CharField(blank=True, choices=[('NC-17', 'NC-17'), ('TV-MA', 'TV-MA'), ('G', 'G'), ('PG-13', 'PG-13'), ('TV-Y', 'TV-Y'), ('R', 'R'), ('PG', 'PG'), ('TV-Y7', 'TV-Y7'), ('TV-14', 'TV-14'), ('TV-Y FV', 'TV-Y FV')], default='', help_text='Select movie/show rating.', max_length=10, verbose_name='Movie/show Rating')),
                ('watch_type', models.CharField(blank=True, choices=[('Movie', 'Movie'), ('Show', 'Show')], default='MOVIE', help_text='Select movie or show.', max_length=10, verbose_name='Watch Type')),
                ('actor', models.ManyToManyField(blank=True, help_text='Enter an actor.', to='showflow.actor')),
                ('genre', models.ManyToManyField(blank=True, help_text='Enter a genre.', to='showflow.genre')),
                ('streaming', models.ManyToManyField(blank=True, help_text='Enter a streaming app name.', to='showflow.streaming')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watches', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]