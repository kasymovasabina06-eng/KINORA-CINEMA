from django.urls import path
from . import views
app_name='movies'
urlpatterns=[path('upcoming/',views.upcoming,name='upcoming'),path('manage/add/',views.movie_create,name='create'),path('manage/<int:movie_id>/edit/',views.movie_update,name='update'),path('manage/<int:movie_id>/delete/',views.movie_delete,name='delete'),path('',views.movie_list,name='list'),path('api/',views.api_movies,name='api'),path('genre/<slug:slug>/',views.genre_detail,name='genre'),path('<int:movie_id>/',views.movie_detail,name='detail')]
