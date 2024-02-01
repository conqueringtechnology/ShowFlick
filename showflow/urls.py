from django.urls import path
from . import views

app_name = 'showflow'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('about/', views.about, name='about'),
    path('help/', views.help_page, name='help'),

    # Showsmovie
    path('showsmovie_list/', views.showsmovie_list, name='showsmovie_list'),
    path('showsmovie/<int:pk>/', views.showsmovie_detail, name='showsmovie_detail'),
    path('showsmovie/new/', views.showsmovie_create, name='showsmovie_create'),
    path('showsmovie/<int:pk>/edit/', views.showsmovie_edit, name='showsmovie_edit'),
    path('showsmovie/<int:pk>/delete/', views.showsmovie_delete, name='showsmovie_delete'),

    # Filter & Search Results and Search Bar
    path('send/', views.send_results, name='send_results'),
    path('search/', views.search_results, name='search_results'),

    # Actor - Genre - Streaming
    path('ags_list/', views.ags_list, name='ags_list'),
    path('actor/new/', views.actor_create, name='actor_create'),
    path('genre/new/', views.genre_create, name='genre_create'),
    path('streaming/new/', views.streaming_create, name='streaming_create'),

    path('actor/<int:pk>/update/', views.actor_edit, name='actor_edit'),
    path('genre/<int:pk>/update/', views.genre_edit, name='genre_edit'),
    path('streaming/<int:pk>/update/', views.streaming_edit, name='streaming_edit'),
    path('actor/<int:pk>/delete/', views.actor_delete, name='actor_delete'),
    path('genre/<int:pk>/delete/', views.genre_delete, name='genre_delete'),
    path('streaming/<int:pk>/delete/', views.streaming_delete, name='streaming_delete'),


]
