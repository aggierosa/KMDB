from django.urls import path

from . import views

urlpatterns = [
    path("movies/", views.MovieView.as_view()),
    path("movies/register/", views.MoviePostAuth.as_view()),
    path("movies/<int:movie_id>/", views.MovieViewDetailAuth.as_view()),
]