from django.urls import path

from .views import RegistrationView, LoginView, GuestProfile

urlpatterns = [
    path("register/", RegistrationView.as_view()),
    path("login/", LoginView.as_view()),
    path("guest-login/", GuestProfile.as_view()),
]