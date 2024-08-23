from django.core.management.base import BaseCommand
from movie.models import Movie 
import os
import json

class Command(BaseCommand):
    help = 'Load movies from movie_descriptions.json into Movie model'

    def handle(self, *args, **kwargs):
        json_file_path = 'movie/management/commands/movies.json'

        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_movies = json.load(f)

        for i in range(100):
            movie = json_movies[i]

            exist = Movie.objects.filter(title=movie['title']).first()
            if 'plot' not in movie or not movie['plot']:
                movie['plot'] = "No description"
            if not exist:
                Movie.objects.create(title = movie['title'], 
                                     image = os.path.abspath('media/movie/images/default.jpg'),
                                     genre = movie['genre'],
                                     year = movie['year'],
                                     description = movie['plot'])