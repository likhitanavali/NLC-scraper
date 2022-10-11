from imdb import IMDb
ia = IMDb()
movie = '10000 B.C.'
movies = ia.search_movie(movie)
print(movies)
id = movies[0].movieID
series = ia.get_movie(id)
print(series.keys())
print(movie, series.data['genres'])
print(movie, series.data['languages'])
print(movie, series.data['countries'])