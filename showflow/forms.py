from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Watch, Genre, Streaming, Actor


# Register user
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

# Watch Form
class WatchForm(forms.ModelForm):
    class Meta:
        model = Watch
        fields = ['title', 'actor', 'genre', 'streaming', 'release_year', 'length', 'stars', 'rating', 'watch_type', 'url', 'description']


# Actor Form
class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if Actor.objects.filter(first_name=first_name, last_name=last_name).exists():
            raise forms.ValidationError("This combination of first name and last name already exists.")

        return cleaned_data

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not first_name:
            raise forms.ValidationError("First name is required.")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not last_name:
            raise forms.ValidationError("Last name is required.")

        return last_name


# Genre Form
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre_name']

    def clean(self):
        cleaned_data = super().clean()
        genre_name = cleaned_data.get('genre_name')

        if Genre.objects.filter(genre_name=genre_name).exists():
            raise forms.ValidationError("This genre name already exists.")

        return cleaned_data

    def clean_genre_name(self):
        genre_name = self.cleaned_data.get('genre_name')

        if not genre_name:
            raise forms.ValidationError("Genre name is required.")

        return genre_name


# Streaming Form
class StreamingForm(forms.ModelForm):
    class Meta:
        model = Streaming
        fields = ['name']

    def clean(self):
        cleaned_data = super().clean()
        streaming_name = cleaned_data.get('name')

        if Streaming.objects.filter(name=streaming_name).exists():
            raise forms.ValidationError("This streaming name already exists.")

        return cleaned_data

    def clean_name(self):
        streaming_name = self.cleaned_data.get('name')

        if not streaming_name:
            raise forms.ValidationError("Streaming name is required.")

        return streaming_name

