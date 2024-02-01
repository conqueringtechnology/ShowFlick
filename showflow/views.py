from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import strip_tags
from showflow.forms import RegistrationForm, WatchForm, ActorForm, GenreForm, StreamingForm
from django.db.models import Q
from .models import Watch, Actor, Genre, Streaming
from .filters import WatchFilter


# home page
def home(request):
    return render(request, "showflow/home.html")


# about page
def about(request):
    return render(request, "showflow/about.html")


# help page
@login_required
def help_page(request):
    return render(request, "showflow/help.html")


# login
def login_user(request):
    return render(request, "registration/login.html")


# register new user
def register_user(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            email = request.POST["email"]
            subject = "Welcome to ShowFlow!"
            message = f"Hello {username} now that you have an account you can start finding shows and movies!"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            form.save()
            messages.success(
                request, "Your account has been created. You can log in now!"
            )
            return redirect("login")
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "registration/register.html", context)


# search and filter movies and shows
# Watch show/movie List View
@login_required
def showsmovie_list(request):
    watch_all = Watch.objects.filter(user=request.user)
    watch_filter = WatchFilter(request.POST, queryset=watch_all)

    context = {
        "form": watch_filter.form,
        "watch_filter": watch_filter,
        "user": request.user
    }
    return render(request, "showflow/showsmovie_list.html", context)

# Watch show/movie Detail View
@login_required
def showsmovie_detail(request, pk):
    watch = get_object_or_404(Watch, pk=pk)

    return render(request, 'showflow/showsmovie_detail.html', {'watch': watch})

# Watch show/movie Create View
@login_required
def showsmovie_create(request):
    if request.method == 'POST':
        form = WatchForm(request.POST)
        if form.is_valid():
            watch = form.save(commit=False)
            watch.user = request.user
            watch.save()
            form.save_m2m()
            messages.success(request, f'The show/movie "{watch.title}" has been successfully added.')
            return redirect('showflow:showsmovie_list')
        else:
            messages.error(request, 'Failed to add the show/movie.')
    else:
        form = WatchForm()

    return render(request, 'showflow/showsmovie_form.html', {'form': form})

# Watch show/movie Edit View
@login_required
def showsmovie_edit(request, pk):
    watch = get_object_or_404(Watch, pk=pk)

    if request.method == 'POST':
        form = WatchForm(request.POST, instance=watch)
        if form.is_valid():
            watch = form.save(commit=False)
            watch.save()
            form.save_m2m()
            messages.success(request, f'The show/movie "{watch.title}" has been successfully updated.')
            return redirect('showflow:send_results')
        else:
            messages.error(request, 'Failed to update the show/movie.')
    else:
        form = WatchForm(instance=watch)
    return render(request, 'showflow/showsmovie_form.html', {'form': form})

# Watch show/movie Delate View
@login_required
def showsmovie_delete(request, pk):
    watch = get_object_or_404(Watch, pk=pk)

    if request.method == 'POST':
        if request.POST.get('confirm_delete') == 'True':
            watch.delete()
            messages.success(request, f'The show/movie "{watch.title}" has been successfully deleted.')
            return redirect('showflow:send_results')
        else:
            messages.error(request, 'Deletion was cancelled.')
    else:
        return render(request, 'showflow/showsmovie_delete.html', {'watch': watch})


# Actor - Genre - Streaming List
# AGS List View
def ags_list(request):
    # Model
    actors = Actor.objects.all()
    genres = Genre.objects.all()
    streamings = Streaming.objects.all()

    # Forms
    actor_form = ActorForm(request.POST)
    genre_form = GenreForm(request.POST)
    streaming_form = StreamingForm(request.POST)

    context = {
        'actors': actors,
        'genres': genres,
        'streamings': streamings,
        'actor_form': actor_form,
        'genre_form': genre_form,
        'streaming_form': streaming_form
    }

    return render(request, 'showflow/ags_list.html', context)


# Actor - Genre - Streaming
# Actor Add
def actor_create(request):
    if request.method == 'POST':
        actor_form = ActorForm(request.POST)

        if actor_form.is_valid():
            actor_form = actor_form.save(commit=False)
            actor_form.save()
            messages.success(request, f'The actor {actor_form.first_name} {actor_form.last_name} has been successfully added.')
            return redirect('showflow:ags_list')
        else:
            # Manage Form and View Messages Together
            # Extract plain text non-field errors
            non_field_errors = actor_form.non_field_errors()

            # Extract plain text field-specific errors without duplicating non-field errors
            field_errors = "\n".join([f"{strip_tags(error)}" for field, error in actor_form.errors.items() if field != '__all__'])

            # Combine non-field errors and field-specific errors
            error_messages = "\n".join([f"{error}" for error in non_field_errors] + [field_errors])

            messages.error(request, f'The actor could not be added. Please correct the following errors:\n{error_messages}')
            return redirect('showflow:ags_list')

    else:
        actor_form = ActorForm()

    context = {'actor_form': actor_form}

    return render(request, 'showflow/ags_list.html', context)

# Genre Add
def genre_create(request):
    if request.method == 'POST':
        genre_form = GenreForm(request.POST)

        if genre_form.is_valid():
            genre_form = genre_form.save(commit=False)
            genre_form.save()
            messages.success(request, f'The genre {genre_form.genre_name} has been successfully added.')
            return redirect('showflow:ags_list')
        else:
            # Manage Form and View Messages Together
            non_field_errors = genre_form.non_field_errors()
            field_errors = "\n".join([f"{strip_tags(error)}" for field, error in genre_form.errors.items() if field != '__all__'])
            error_messages = "\n".join([f"{error}" for error in non_field_errors] + [field_errors])
            messages.error(request, f'The genre could not be added. Please correct the following errors:\n{error_messages}')

            return redirect('showflow:ags_list')

    else:
        genre_form = GenreForm()

    context = {'genre_form': genre_form}

    return render(request, 'showflow/ags_list.html', context)

# Streaming Add
def streaming_create(request):
    if request.method == 'POST':
        streaming_form = StreamingForm(request.POST)

        if streaming_form.is_valid():
            streaming_form = streaming_form.save(commit=False)
            streaming_form.save()
            messages.success(request, f'The streaming {streaming_form.name} has been successfully added.')
            return redirect('showflow:ags_list')

        else:
            # Manage Form and View Messages Together
            non_field_errors = streaming_form.non_field_errors()
            field_errors = "\n".join([f"{strip_tags(error)}" for field, error in streaming_form.errors.items() if field != '__all__'])
            error_messages = "\n".join([f"{error}" for error in non_field_errors] + [field_errors])
            messages.error(request, f'The streaming could not be added. Please correct the following errors:\n{error_messages}')

            return redirect('showflow:ags_list')

    else:
        streaming_form = StreamingForm()

    context = {'streaming_form': streaming_form}

    return render(request, 'showflow/ags_list.html', context)


# Actor - Genre - Streaming Update
# Actor Update
@login_required
def actor_edit(request, pk):
    actor_fullname = get_object_or_404(Actor, pk=pk)

    if request.method == 'POST':
        actor_form = ActorForm(request.POST, instance=actor_fullname)
        if actor_form.is_valid():
            actor_form.save(commit=False)
            actor_form.save()
            messages.success(request, f'The actor has been successfully updated.')
            return redirect('showflow:ags_list')
        else:
            # Manage Form and View Messages Together
            non_field_errors = actor_form.non_field_errors()
            field_errors = "\n".join([f"{strip_tags(error)}" for field, error in actor_form.errors.items() if field != '__all__'])
            error_messages = "\n".join([f"{error}" for error in non_field_errors] + [field_errors])
            messages.error(request,f'Failed to update the actor. Please correct the following errors:\n{error_messages}')
    else:
        actor_form = ActorForm(instance=actor_fullname)

    context = {
        'actor_form': actor_form,
    }

    return render(request, 'showflow/actor_update.html', context)

# Genre Update
@login_required
def genre_edit(request, pk):
    genre = get_object_or_404(Genre, pk=pk)

    if request.method == 'POST':
        genre_form = GenreForm(request.POST, instance=genre)
        if genre_form.is_valid():
            genre_form.save(commit=False)
            genre_form.save()
            messages.success(request, f'The genre has been successfully updated.')
            return redirect('showflow:ags_list')
        else:
            # Manage Form and View Messages Together
            non_field_errors = genre_form.non_field_errors()
            field_errors = "\n".join([f"{strip_tags(error)}" for field, error in genre_form.errors.items() if field != '__all__'])
            error_messages = "\n".join([f"{error}" for error in non_field_errors] + [field_errors])
            messages.error(request,f'Failed to update the genre. Please correct the following errors:\n{error_messages}')
    else:
        genre_form = GenreForm(instance=genre)

    context = {
        'genre_form': genre_form,
    }

    return render(request, 'showflow/genre_update.html', context)

# Streaming Update
@login_required
def streaming_edit(request, pk):
    streaming = get_object_or_404(Streaming, pk=pk)

    if request.method == 'POST':
        streaming_form = StreamingForm(request.POST, instance=streaming)
        if streaming_form.is_valid():
            streaming_form.save(commit=False)
            streaming_form.save()
            messages.success(request, f'The streaming has been successfully updated.')
            return redirect('showflow:ags_list')
        else:
            # Manage Form and View Messages Together
            non_field_errors = streaming_form.non_field_errors()
            field_errors = "\n".join([f"{strip_tags(error)}" for field, error in streaming_form.errors.items() if field != '__all__'])
            error_messages = "\n".join([f"{error}" for error in non_field_errors] + [field_errors])
            messages.error(request,f'Failed to update the streaming. Please correct the following errors:\n{error_messages}')
    else:
        streaming_form = GenreForm(instance=streaming)

    context = {
        'streaming_form': streaming_form,
    }

    return render(request, 'showflow/streaming_update.html', context)


# Actor Delete
@login_required
def actor_delete(request, pk):
    actor = get_object_or_404(Actor, pk=pk)

    if request.method == 'POST':
        if request.POST.get('confirm_delete') == 'True':
            actor.delete()
            messages.success(request, f'The actor "{actor.first_name} {actor.last_name}" has been successfully deleted.')
            return redirect('showflow:ags_list')
        else:
            messages.error(request, 'Deletion was cancelled.')
    else:
        return render(request, 'showflow/actor_delete.html', {'actor': actor})

# Genre Delete
@login_required
def genre_delete(request, pk):
    genre = get_object_or_404(Genre, pk=pk)

    if request.method == 'POST':
        if request.POST.get('confirm_delete') == 'True':
            genre.delete()
            messages.success(request, f'The genre "{genre.genre_name}" has been successfully deleted.')
            return redirect('showflow:ags_list')
        else:
            messages.error(request, 'Deletion was cancelled.')
    else:
        return render(request, 'showflow/genre_delete.html', {'genre': genre})

# Streaming Delete
@login_required
def streaming_delete(request, pk):
    streaming = get_object_or_404(Streaming, pk=pk)

    if request.method == 'POST':
        if request.POST.get('confirm_delete') == 'True':
            streaming.delete()
            messages.success(request, f'The streaming "{streaming.name}" has been successfully deleted.')
            return redirect('showflow:ags_list')
        else:
            messages.error(request, 'Deletion was cancelled.')
    else:
        return render(request, 'showflow/streaming_delete.html', {'streaming': streaming})


# email search and filter results
@login_required
def send_results(request):
    watch_all = Watch.objects.filter(user=request.user)
    watch_filter = WatchFilter(request.POST, queryset=watch_all)

    if request.method == "POST":
        email = request.POST.get("yessend")
        if email is not None:
            username = request.user.first_name
            htmloutput = " "
            for watch in watch_filter.qs:
                htmloutput += (
                    f"<tr><td>{watch.title}</td>"
                    + f"<td>{watch.display_actor()}</td>"
                    + f"<td>{watch.display_genre()}</td>"
                    + f"<td>{watch.display_streaming()}</td>"
                    + f"<td>{watch.release_year}</td>"
                    + f"<td>{watch.length}</td>"
                    + f"<td>{watch.stars}</td>"
                    + f"<td>{watch.rating}</td>"
                    + f"<td>{watch.watch_type}</td>"
                    + f'<td><a href="{watch.url}">Details</a></td></tr>'
                )

            subject, from_email, to = (
                f"Your Movies & Shows list!",
                "settings.EMAIL_HOST_USER",
                email,
            )
            text_content = "This is your requested movie & show list."
            html_content = (
                f"<h1>ShowFlow Movie & Shows List</h1><p>Hello {username};</p>"
                f"<p>This is your requested movie & show list. Click on details to see more details on the movie or show.</p>"
                f"<h3>Movies & Shows</h3>"
                f"<table><tr><th>Title</th><th>Actor</th><th>Genre</th><th>Streaming</th>"
                f"<th>Year Released</th><th>Movie/Show Length</th><th>Movie/Show Rating</th>"
                f"<th>Movie/Show Stars</th><th>Watch Type</th><th>Details</th></tr><hr>"
                f"{htmloutput}</table>"
            )

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        else:
            context = {
                "watch_filter": watch_filter,
            }
            return render(request, "showflow/email_results.html", context)
    context = {
        "watch_filter": watch_filter,
    }
    return render(request, "showflow/email_results.html", context)


# search bar
@login_required
def search_results(request):
    user_query = Watch.objects.filter(user=request.user)
    searched = request.POST.get("searched")

    if searched:
        search_results = user_query.filter(
            Q(title__icontains=searched)
            | Q(actor__last_name__icontains=searched)
            | Q(genre__genre_name__icontains=searched)
            | Q(streaming__name__icontains=searched)
            | Q(length__icontains=searched)
            | Q(rating__exact=searched)
            | Q(watch_type__exact=searched)
        ).distinct()
    else:
        search_results = user_query

    context = {
        "searched": searched,
        "query": search_results,
    }
    return render(request, "showflow/search_results.html", context)
