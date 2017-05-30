from recommendation.models import *
import json
import hashlib

def get_list_id_by_user(user_id):
    lists = []
    for item in List.objects.raw("SELECT list_ID FROM list WHERE user_id = %s", [user_id]):
        lists.append(item.list_id)
    return lists

def movie_by_user_list(user_id, list_name):
    list_id = 0
    for item in Type.objects.raw("SELECT * FROM type WHERE type_name = %s", [list_name]):
        type_id = item.type_id

    for item in List.objects.filter(user_id = user_id, type_id = type_id):
        list_id = item.list_id

    movie_list = Movie.objects.raw("SELECT * from movie INNER JOIN movie_list ON list_id = %s AND movie_list.movie_id = movie.movie_id", [list_id])
    return movie_list

def get_rated_movies_by_user(user_id):
    movies =[]
    rate_list = {}

    for item in movie_by_user_list(user_id, 'watchedlist'):
        movies.append(item.movie_id)

    for movie in movies:
        rate = get_rate_by_movie(movie, user_id)
        rate_list.update({movie: rate})

    return rate_list

def get_rate_by_movie(movie_id, user_id):
    rate_id = 0
    movie_rate = 0
    for item in Rating.objects.raw("SELECT * FROM rating WHERE rating.user_id = %s AND movie_id = %s", [user_id, movie_id]):
        rate_id = item.rate_id

    for item in Rate.objects.raw("SELECT * FROM rate WHERE rate_id = %s", [rate_id]):
        movie_rate = item.rate

    return movie_rate

def get_list_by_user(user, list_type):
    for item in List.objects.raw("SELECT list_ID FROM list WHERE user_id = %s AND type_id = %s", [user, list_type]):
        list_id = item.list_id
    return list_id
    
def get_movie_by_user(user_id):
    movies =[]
   
    for item in movie_by_user_list(user_id, 'watchedlist'):
        movies.append(item.movie_id)
    return movies

def get_user_by_email(email):
    user = User.objects.filter(email = email)

    return user[0].user_id

def get_tmdb_movies_id():
    movies = []

    for item in Movie.objects.all():
        movies.append(item.tmdb_movie_id)

    return movies

def get_tmdb_movie_id_by_movie(movie_id):
    for item in Movie.objects.raw("SELECT * FROM movie WHERE movie_id = %s", [movie_id]):
        return item.tmdb_movie_id

def get_movie_id_by_tmdb_id(tmdb_movie_id):
    for item in Movie.objects.raw("SELECT * FROM movie WHERE tmdb_movie_id = %s", [tmdb_movie_id]):
        return item.movie_id

def get_tmdb_movies_id_by_user(user):
    lists_id = get_list_id_by_user(user)
    movies = []

    for item in lists_id:
        for movie in Movie.objects.raw("SELECT * from movie INNER JOIN movie_list ON list_id = %s AND movie_list.movie_id = movie.movie_id", [item]):
            movies.append(movie.tmdb_movie_id)
    
    return movies

def is_movie_on_list (user_id, movie_id, list_type):
    list_id = get_list_by_user(user_id, list_type)

    movie_list = MovieList.objects.filter(movie_id = movie_id, list_id = list_id)

    if not movie_list:
        return False
    else:
        return True

def get_movie_title(movie_id):
    movie = Movie.objects.filter(movie_id = movie_id)

    return movie[0].tmdb_title

def get_movie_poster(movie_id):
    movie = Movie.objects.filter(movie_id = movie_id)

    return movie[0].tmdb_poster

def get_movie_tmdb_id(movie_id):
    movie = Movie.objects.filter(movie_id = movie_id)

    return movie[0].tmdb_movie_id

def get_watchedlist (user):
    watched_list = []
    list_id = get_list_by_user(user, 3)
    movies = MovieList.objects.filter(list_id = list_id)

    for m in movies:
        watched_list.append({
            'movie_id': m.movie_id,
            'tmdb_movie_id': get_movie_tmdb_id(m.movie_id),
            'title': get_movie_title(m.movie_id),
            'poster': get_movie_poster(m.movie_id),
            'rating': get_rate_by_movie(m.movie_id, user)
        })

    return json.dumps(watched_list)

def get_watchlist(user):
    watchlist = []
    list_id = get_list_by_user(user, 2)
    movies = MovieList.objects.filter(list_id = list_id)

    for m in movies:
        watchlist.append({
            'movie_id': m.movie_id,
            'tmdb_movie_id': get_movie_tmdb_id(m.movie_id),
            'title': get_movie_title(m.movie_id),
            'poster': get_movie_poster(m.movie_id),
        })

    return json.dumps(watchlist)

def jsonify_reco_list(user_id, list_name):
    movies = movie_by_user_list(user_id, list_name)
    reco_list = []

    for movie in movies:
        reco_list.append({'tmdb_movie_id': movie.tmdb_movie_id, 'movie_id': movie.movie_id, 'tmdb_poster': movie.tmdb_poster, 'tmdb_title': movie.tmdb_title,})
    
    return json.dumps(reco_list)

def get_genres_by_user(user_id):
    profile_id = Profile.objects.filter(user_id = user_id)
    profile_id = profile_id[0].profile_id

    genre_id = ProfileGenre.objects.filter(profile_id = profile_id)

    genre_1 = Genre.objects.filter(genre_id = genre_id[0].genre_id)
    genre_2 = Genre.objects.filter(genre_id = genre_id[1].genre_id)
    genre_3 = Genre.objects.filter(genre_id = genre_id[2].genre_id)

    genres = {'genre_1': genre_1[0].tmdb_genre_id, 'genre_2': genre_2[0].tmdb_genre_id,'genre_3': genre_3[0].tmdb_genre_id}
    return genres

def user_exists(user_email):
    user = User.objects.filter(email = user_email)

    if not user:
        return False
    else:
        return True

def get_profile_id(user_id):
    profile = Profile.objects.filter(user_id = user_id)

    return profile[0].profile_id

def get_profile_genre_id(profile_id):
    profile = ProfileGenre.objects.filter(profile_id = profile_id)

    profile_genre = []
    for p in profile:
        profile_genre.append(p.profile_genre_id)

    return profile_genre

#UPDATE, DELETE, INSERT

def add_rating_to_movie(user_id, movie_id, local_rate_id):
    rating_query = Rating.objects.filter(movie_id = movie_id, user_id= user_id)

    if not rating_query:
        user_rating = Rating(user_id = user_id, movie_id = movie_id, rate_id = local_rate_id)
        user_rating.save()
    else:
        for item in rating_query:
            user_rating = Rating(rating_id = item.rating_id, user_id = user_id, movie_id = movie_id, rate_id = local_rate_id)
            user_rating.save()

def remove_movie_from_list(user_id, movie_id, list_type):
    list_id = get_list_by_user(user_id, list_type)

    MovieList.objects.filter(movie_id = movie_id, list_id = list_id).delete()

def remove_rating(user_id, movie_id):
    Rating.objects.filter(movie_id = movie_id, user_id = user_id).delete()

def remove_watched(user_id, movie_id, list_type):
    remove_movie_from_list(user_id, movie_id, list_type)

    remove_rating(user_id, movie_id)

def add_to_list_external(user_id, tmdb_movie_id, tmdb_poster, tmdb_title, list_type):
    movie = Movie.objects.filter(tmdb_movie_id = tmdb_movie_id)
    if movie:
        movie_id = movie[0].movie_id
        add_to_list (user_id, movie_id, list_type)
    else:
        new_movie = Movie(tmdb_movie_id = tmdb_movie_id, tmdb_poster = tmdb_poster, tmdb_title = tmdb_title)
        new_movie.save()
        movie = Movie.objects.filter(tmdb_movie_id = tmdb_movie_id)
        if movie:
            movie_id = movie[0].movie_id
            add_to_list (user_id, movie_id, list_type)
        else:
            print('Errro while adding new movie to list')

def add_to_list (user_id, movie_id, list_type):
    list_id = get_list_by_user(user_id, list_type)
    is_on_list = MovieList.objects.filter(movie_id = movie_id, list_id = list_id)

    #If in recommendation list, remove it
    if is_movie_on_list (user_id, movie_id, 1):
        remove_movie_from_list(user_id, movie_id, 1)
    
    if not is_on_list:
        movie_list_entry = MovieList(movie_id = movie_id, list_id = list_id)
        movie_list_entry.save()

def rate_movie (user_id, movie_id, local_rate_id):

    #add rating
    add_rating_to_movie(user_id, movie_id, local_rate_id)

    #check if it is on watchlist and remove it
    if is_movie_on_list(user_id, movie_id, 2):
        remove_movie_from_list(user_id, movie_id, 2)

    #add to watched list
    add_to_list (user_id, movie_id, 3)

def rate_external_movie (user_id, user_rating, tmdb_movie_id, tmdb_poster, tmdb_title):
    movie = Movie.objects.filter(tmdb_movie_id = tmdb_movie_id)

    if movie:
        movie_id = movie[0].movie_id
        rate_movie (user_id, movie_id, user_rating)
        return True
    else:
        new_movie = Movie(tmdb_movie_id = tmdb_movie_id, tmdb_poster = tmdb_poster, tmdb_title = tmdb_title)
        new_movie.save()
        movie = Movie.objects.filter(tmdb_movie_id = tmdb_movie_id)
        if movie:
            movie_id = movie[0].movie_id
            rate_movie (user_id, movie_id, user_rating)
            return True
        else:
            return false

def register_user(name, email, password):
    user_id = create_user(name, email, password)
   
    create_list_to_user(user_id, 1)
    create_list_to_user(user_id, 2)
    create_list_to_user(user_id, 3)

    return user_id

def create_user(name, email, password):
    hash_password = hashlib.sha224(password).hexdigest()

    user = User(name = name, email = email, password = hash_password, description = '')
    user.save()
    user_id = get_user_id(email)

    return user_id

def create_user_profile(user_id):
    profile = Profile(user_id = user_id)
    profile.save()
    profile_id = get_profile_id(user_id)

    return profile_id

def get_genre_id(genre_tmdb_id):
    genre = Genre.objects.filter(tmdb_genre_id = genre_tmdb_id)
    genre_id = genre[0].genre_id

    return genre_id

def add_genres_to_user(profile_id, genres):

    for genre in genres:
        profile_genre = ProfileGenre(profile_id = profile_id, genre_id = genre)
        profile_genre.save()

def create_list_to_user(user_id, type_id):
    user_list = List(user_id = user_id, type_id = type_id)
    user_list.save()

def update_user_info(user_id, email, name, password):
    old_user = User.objects.filter(user_id = user_id)
    if not email or email == ' ':
        email = old_user[0].email
    if not name or name == ' ':
        name = old_user[0].name
    if not password or password == ' ':
        password = old_user[0].password
    else:
        password = hashlib.sha224(password).hexdigest()

    user = User(user_id = user_id, name = name, email = email, password = password)
    user.save()

def update_user_genres(user_id, firstG, secondG, thirdG):
    profile_id = get_profile_id(user_id)
    profile_genres_id = get_profile_genre_id(profile_id)

    firstG = get_genre_id(firstG)
    secondG = get_genre_id(secondG)
    thirdG = get_genre_id(thirdG)

    g = ProfileGenre(profile_genre_id = profile_genres_id[0], profile_id = profile_id, genre_id = firstG)
    g.save()

    g = ProfileGenre(profile_genre_id = profile_genres_id[1], profile_id = profile_id, genre_id = secondG)
    g.save()

    g = ProfileGenre(profile_genre_id = profile_genres_id[2], profile_id = profile_id, genre_id = thirdG)
    g.save()

#AUTHENTICATION HANDLERS

def authenticate_user(email, password):
    hash_password = hashlib.sha224(password).hexdigest()
    #hash_password = password

    user = User.objects.filter(email = email, password = hash_password)

    if user:
        return True
    else:
        return False

def get_user(email):
    user = User.objects.filter(email = email)

    user_info = {'user_id': user[0].user_id, 'name': user[0].name, 'email': user[0].email,}

    return json.dumps(user_info)

def get_user_id(email):
    user = User.objects.filter(email = email)

    return user[0].user_id

#PROFILE HANDLERS

def get_user_details(user_id):
    user = User.objects.filter(user_id = user_id)
    genres = get_genres_by_user(user_id)

    genres = [ genres['genre_1'],  genres['genre_2'], genres['genre_3']]

    user_details = {'name': user[0].name, 'email': user[0].email, 'genres': genres }

    return json.dumps(user_details)

#COMMENTS HANDLERS

def get_comments(movie_tmdb_id):
    movie_id = get_movie_id_by_tmdb_id(movie_tmdb_id)
    comments = Comments.objects.filter(movie_id = movie_id)
    commnets_by_movie = []

    for comment in comments:
        user = User.objects.filter(user_id = comment.user_id)
        name = user[0].name
        rate = get_rate_by_movie(movie_id, comment.user_id)
        commnets_by_movie.append({"comment_id": comment.comment_id, "user_name": name,"comment": comment.comment, "rate": rate})

    return json.dumps(commnets_by_movie)

def add_comment(movie_tmdb_id, user_id, comment):
    movie_id = get_movie_id_by_tmdb_id(movie_tmdb_id)

    comment = Comments(movie_id = movie_id, user_id = user_id, comment = comment)
    comment.save()

def delete_comment(comment_id):
    Comments.objects.filter(comment_id = comment_id).delete()

    if not Comments.objects.filter(comment_id = comment_id):
        return True
    else:
        return False

def get_rated_movies():
    ratings = Rating.objects.all()
    rated_movies = []

    for movie in ratings:
        movie_info = Movie.objects.filter(movie_id = movie.movie_id)
        if movie_info:
            rated_movies.append({'movie_id': movie_info[0].movie_id, 'title': movie_info[0].tmdb_title, 'poster': movie_info[0].tmdb_poster})

    return json.dumps(rated_movies)

