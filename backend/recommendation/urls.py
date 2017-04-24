from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^movies/$', views.MovieView.as_view(), name='movies'),
    url(r'^reco/$', views.RecoView.as_view(), name='recommendation'),
    url(r'^main/$', views.main, name='main'),
    url(r'^full-recommendation/$', views.fullreco, name='fullreco'),
    url(r'^ratemovie/$', views.ratemovie, name='ratemovie'),
    url(r'^moviedetails/$', views.moviedetails, name='moviedetails'),
    url(r'^addwatchlist/$', views.add_watchlist, name='addwatchlist'),
    url(r'^addwatchlistexternal/$', views.add_watchlist_external, name='addwatchlistexternal'),
    url(r'^rateexternalmovie/$', views.rate_external, name='rateexternalmovie'),
    url(r'^watchedlist/$', views.show_watched_list, name='watchedlist'),
    url(r'^getwatchedlist/$', views.get_watched_list, name='getwatchedlist'),
    url(r'^removefromwatchedlist/$', views.remove_from_watched_list, name='removefromwatchedlist'),
    url(r'^removefromwatchlist/$', views.remove_from_watchlist, name='removefromwatchlist'),
    url(r'^watchlist/$', views.show_watchlist, name='watchlist'),
    url(r'^getwatchlist/$', views.get_watch_list, name='getwatchlist'),
    url(r'^filters/$', views.show_filters, name='filters'),
    url(r'^login/$', views.show_login, name='login'),
    url(r'^singup/$', views.show_singup, name='singup'),
    url(r'^authentication/$', views.get_auth, name='authentication'),
    url(r'^registration/$', views.registration, name='registration'),

    


    

]

urlpatterns = format_suffix_patterns(urlpatterns)