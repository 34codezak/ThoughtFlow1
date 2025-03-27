from django.urls import path
from . import views
from journal.views import signup, home, user_logout
from django.contrib.auth.views import LoginView
from .views import signup, user_logout

urlpatterns = [
    path("signup/", views.signup, name="signup"), # Calls the signup function in views.py to handle the signup process
    path("login/", LoginView.as_view(), name="login"), # Uses Django's built-in LoginView but with a custom template
    path("logout/", views.user_logout, name="logout"), # Calls the user_logout function in views.py to handle the logout process and redirect them
    path("", views.home, name="home"), # Calls the home function in views.py to render the home page
    path("update_profile/", views.update_profile, name="update_profile"), # Calls the update_profile function in views.py to render the update profile page
]

