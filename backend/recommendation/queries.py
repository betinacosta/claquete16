from recommendation.models import Movie, User, List, Rating, Rate, MovieList, Type

def movie_by_user_list(user_id, list_name):
    
    for item in Type.objects.raw("SELECT * FROM type WHERE type_name = %s", [list_name]):
        type_id = item.type_id;

    for item in List.objects.raw("SELECT list_ID FROM list WHERE user_id = %s AND type_id = %s", [user_id, type_id]):
        list_id = item.list_id

    return Movie.objects.raw("SELECT * from movie INNER JOIN movie_list ON list_id = %s AND movie_list.movie_id = movie.movie_id", [list_id])