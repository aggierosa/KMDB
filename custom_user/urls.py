from django.urls import path

from rest_framework.authtoken import views
from .views import LoginView, UserView

urlpatterns = [
    path("users/login/", LoginView.as_view()),
    path("users/", UserView.as_view())
]