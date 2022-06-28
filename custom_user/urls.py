from django.urls import path

from .views import LoginBView, UserView, UserAuthView, UserDetailAuthView


urlpatterns = [
    path("users/login/", LoginBView.as_view()),
    path("users/register/", UserView.as_view()),
    path("users/", UserAuthView.as_view()),
    path("users/<int:user_id>/", UserDetailAuthView.as_view())
]