from django.shortcuts import render
from django.http import HttpResponse
from movie.models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchMovie')
    movies = Movie.objects.all()
    new_movies = {}

    if searchTerm:
        print(movies.values_list('description', flat=True))
        movies = movies.filter(title__icontains=searchTerm)
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})

def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def statistics_view(request):
    matplotlib.use("Agg")
    all_movies = Movie.objects.all()

    movie_counts_by_year = {}
    movie_counts_by_genre = {}

    for movie in all_movies:
        year = movie.year if movie.year else "None"
        genre = movie.genre.split(",")[0] if movie.genre else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
            print(year, movie.title)
        else:
            movie_counts_by_year[year] = 1
        
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
            print(genre, movie.title)
        else:
            movie_counts_by_genre[genre] = 1

    bar_width = 0.5
    plt.bar(movie_counts_by_genre.keys(), movie_counts_by_genre.values(), width=bar_width, align='center')

    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=90)

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png).decode('utf-8')


    movie_counts_by_year = dict(sorted(movie_counts_by_year.items()))
    bar_width = 0.5
    plt.bar(movie_counts_by_year.keys(), movie_counts_by_year.values(), width=bar_width, align='center')

    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'statistics.html', {'graphic_genre': graphic_genre, 'graphic_year':graphic_year})