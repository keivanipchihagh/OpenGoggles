from django.urls import path
from .views import *

urlpatterns = [
    # Reports
    path('genre_popularity', genre_popularity, name='genre_popularity'),
    path('actors_crosstab_genres', actors_crosstab_genres, name='actors_crosstab_genres'),
    path('actors_rollup_genres', actors_rollup_genres, name='actors_rollup_genres'),
    path('select_movies', select_movies, name='select_movies'),

    # Functions
    path('movies_by_actor', movies_by_actor, name='movies_by_actor'),
    path('awards_per_actors', awards_per_actors, name='awards_per_actors'),
    path('rents_between', rents_between, name='rents_between'),

    # Triggers
    path('add_purchase', add_purchase, name='add_purchase'),
    path('add_movie', add_movie, name='add_movie'),
]
